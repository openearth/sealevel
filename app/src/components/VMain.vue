<template>
  <v-app id="sea-level-app">
    <v-toolbar light class="pink">
      <v-toolbar-side-icon light @click.native.stop="nav2 = !nav2" />
      <v-toolbar-logo>
        <!-- <img src="static/images/logo.svg" class="logo"> -->
      </v-toolbar-logo>
    </v-toolbar>
    <v-navigation-drawer persistent light v-model="nav2">
      <v-list class="pt-0">
        <v-list-item>
          <v-list-tile avatar tag="div">
            <v-list-tile-avatar>
              <img src="static/images/logo.svg" class="logo">
            </v-list-tile-avatar>
            <v-list-tile-content>
              <v-list-tile-title>Sea-level monitor</v-list-tile-title>
            </v-list-tile-content>
            <v-list-tile-action>
              <v-btn icon @click.native.stop="nav2 = !nav2">
                <v-icon>chevron_left</v-icon>
              </v-btn>
            </v-list-tile-action>
          </v-list-tile>
        </v-list-item>
        <v-divider></v-divider>
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

  .logo {
  max-height: 30px;
  }

</style>
