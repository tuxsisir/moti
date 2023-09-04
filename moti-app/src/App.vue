<script setup>
import { ref, onMounted, computed, reactive } from "vue";
import * as vNG from "v-network-graph"
import { defineConfigs } from "v-network-graph"

import NavHeader from './components/NavHeader.vue'

import dagre from "dagre/dist/dagre.min.js"

import PersonForm from './components/Forms/PersonForm.vue'
import RelationForm from './components/Forms/RelationForm.vue'

import ErrorNotification from './components/ErrorNotification.vue'


const errorResponse = ref({});

const nodes = ref({});
const edges = ref({});

// active node and edges
const activeNode = ref(null);
const activeEdge = ref(null);

// hide help
const hideHelp = ref(false);

// button actions - control center
const addPerson = ref(false);
const addRelation = ref(false);
const updatePerson = ref(false);

async function fetchPersons() {
  await fetch('http://localhost:8000/users/nodes/')
    .then(response => response.json())
    .then((data) => {
      nodes.value = data.nodes
      edges.value = data.edges
    });
}

const eventHandlers = {
  "node:click": ({ node }) => {
    // toggle
    nodes.value[node].active = !nodes.value[node].active
    activeNode.value = node;
    activeEdge.value = null;
    addPerson.value = false;
    updatePerson.value = false;
  },
  "edge:click": ({ edge }) => {
    // toggle
    activeEdge.value = edge;
    activeNode.value = null
  },
}

const layouts = reactive({
  nodes: {},
})

const configs = defineConfigs({
  view: {
    layoutHandler: new vNG.GridLayout({ grid: 12 }),
    autoPanAndZoomOnLoad: "fit-content",
  },
  node: {
    normal: {
      color: "#4466cc88",
    },
    selectable: true,
    label: {
      visible: true,
      direction: "south",
      directionAutoAdjustment: true,
    },
  },
  edge: {
    selectable: true,
    normal: {
      color: "#aaa",
      width: 2,
    },
    margin: 4,
    marker: {
      source: {
        type: "circle",
        width: 4,
        height: 4,
      },
      target: {
        type: "circle",
        width: 4,
        height: 4,
      },
    },
  },
})


const activeNodeUser = computed(() => {
  return nodes.value[activeNode.value]
})
const activeEdgeRelation = computed(() => {
  return edges.value[activeEdge.value]
})

function deleteRelation() {
  fetch('http://localhost:8000/relation/' + activeEdgeRelation.value.id + "/", {
    method: "DELETE",
    headers: { "Content-Type": "application/json" },
  }).then((_) => {
    fetchPersons();
    activeEdge.value = null;
  })
}

function deletePerson() {
  fetch('http://localhost:8000/users/' + activeNodeUser.value.id + "/", {
    method: "DELETE",
    headers: { "Content-Type": "application/json" },
  }).then((_) => {
    fetchPersons();
    activeNode.value = null;
  })
}
const zoomLevel = ref(1.5);
const graph = ref(null)
const nodeSize = 40

function layout(direction) { // : "TB" | "LR"
  if (Object.keys(nodes).length <= 1 || Object.keys(edges).length == 0) {
    return
  }

  // convert graph
  // ref: https://github.com/dagrejs/dagre/wiki
  const g = new dagre.graphlib.Graph()
  // Set an object for the graph label
  g.setGraph({
    rankdir: direction,
    nodesep: nodeSize * 2,
    edgesep: nodeSize,
    ranksep: nodeSize * 2,
  })
  // Default to assigning a new object as a label for each new edge.
  g.setDefaultEdgeLabel(() => ({}))

  // Add nodes to the graph. The first argument is the node id. The second is
  // metadata about the node. In this case we're going to add labels to each of
  // our nodes.
  Object.entries(nodes.value).forEach(([nodeId, node]) => {
    g.setNode(nodeId, { label: node.name, width: nodeSize, height: nodeSize })
  })

  // Add edges to the graph.
  Object.values(edges.value).forEach(edge => {
    g.setEdge(edge.source, edge.target)
  })

  dagre.layout(g)

  g.nodes().forEach((nodeId) => {
    // update node position
    const x = g.node(nodeId).x
    const y = g.node(nodeId).y
    layouts.nodes[nodeId] = { x, y }
  })
}

function updateLayout(direction) { // : "TB" | "LR"
  // Animates the movement of an element.
  graph.value?.transitionWhile(() => {
    layout(direction)
  })
  resetControlCenter();
}

function resetControlCenter() {
  errorResponse.value = {};
  addPerson.value = false;
  updatePerson.value = false;
  activeNode.value = null;
  activeEdge.value = null;
}

async function onSuccessResponse() {
  await fetchPersons();
  updateLayout("TB")
  resetControlCenter();
}

function onErrorResponse(response) {
  errorResponse.value = response;
}

onMounted(async () => {
  await fetchPersons();
  updateLayout("TB");
})
</script>

<template>
  <div class="is-fullheight">
    <NavHeader></NavHeader>
    <div class="container">
      <ErrorNotification :error-response="errorResponse"></ErrorNotification>
      <div class="m-5">
        <h5 class="is-size-5 my-3">Control Center</h5>
        <div class="is-flex is-flex-wrap-wrap">
          <button class="button is-link is-light" @click="addPerson = !addPerson">Add new Person</button>
          <button class="button is-link is-light" @click="updateLayout('TB')">Reset Graph</button>
          <button v-if="activeEdge" @click="deleteRelation" class="button is-danger is-light">Delete Relation</button>
          <button v-if="activeNode" class="button is-warning is-light" @click="addRelation = !addRelation">
            Add Relation
          </button>
          <button v-if="activeNode" class="button is-warning is-light" @click="updatePerson = !updatePerson">
            Update Person
          </button>
          <button v-if="activeNode" @click="deletePerson" class="button is-danger is-light">Delete Person</button>
        </div>

      </div>
      <div class="m-5">
        <PersonForm v-if="addPerson || updatePerson" :active-user="activeNodeUser" @success="onSuccessResponse"
          @error="onErrorResponse"></PersonForm>
        <RelationForm v-if="addRelation" @success="onSuccessResponse" @error="onErrorResponse" :users="nodes">
        </RelationForm>
      </div>
      <div class="container m-5">
        <h5 class="is-size-5 mb-4">Graph</h5>
        <div v-if="!hideHelp" class="notification">
          <button class="delete" @click="hideHelp = true"></button>
          <ul>
            <li class="is-italic">Please click on the nodes and edges to play around with the relationships.</li>
          </ul>
        </div>
        <v-network-graph v-model:zoom-level="zoomLevel" ref="graph" class="graph is-fullheight" :nodes="nodes"
          :edges="edges" :layouts="layouts" :configs="configs" :event-handlers="eventHandlers">
          <template #edge-label="{ edge, ...slotProps }">
            <v-edge-label :text="edge.label" align="center" vertical-align="above" v-bind="slotProps" />
          </template>
        </v-network-graph>
      </div>
    </div>
  </div>
</template>

<style>
.is-flex button {
  margin-right: 12px;
  margin-bottom: 12px;
}

.graph {
  border: 1px solid black;
  height: 500px;
}
</style>
