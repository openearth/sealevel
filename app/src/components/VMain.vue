<template>
  <v-app id="sea-level-app" top-toolbar sidebar-under-toolbar>
    <v-toolbar>
      <v-toolbar-side-icon @click.native.stop="nav2 = !nav2" />
      <v-toolbar-logo>Toolbar</v-toolbar-logo>
    </v-toolbar>
    <v-navigation-drawer temporary v-model="nav2">
        <v-list-tile>
          <!-- spacer, bug in vuetify -->
        </v-list-tile>
        <v-list>
          <v-list-item v-for="i in 3" :key="i">
            <v-list-tile>
              <v-list-tile-title>Item {{ i }}</v-list-tile-title>
            </v-list-tile>
          </v-list-item>
        </v-list>
      </v-navigation-drawer>
    <main>

        <v-container fluid>
          <v-layout row wrap>
            <v-flex xs4>
              <slr-indicators></slr-indicators>
            </v-flex>
            <v-flex xs4>
              <v-card>
                <v-card-text>
                  <div>Publications and reports</div>
                </v-card-text>
              </v-card>
            </v-flex>
            <v-flex xs4>
              <v-card>
                <v-card-text>
                  <div>Map</div>
                </v-card-text>
              </v-card>
            </v-flex>

          </v-layout>
        </v-container>
    </main>
  </v-app>
</template>

<script src="./v-main.js"></script>
<style>
  @import '~normalize.css/normalize.css';
  @import '~sanitize.css/sanitize.css';
  @import '~material-design-icons/iconfont/material-icons.css';
  @import '~vuetify/dist/vuetify.min.css';
</style>
