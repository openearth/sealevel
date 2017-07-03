<template>
  <v-card>
    <v-card-row class="">
      <v-card-title>Sea-level monitor</v-card-title>
    </v-card-row>
    <v-card-text>
      <v-list three-line>
        <template v-for="item in indicators">
          <v-subheader v-if="item.header" v-text="item.header"/>
          <v-divider v-else-if="item.divider" v-bind:inset="item.inset"/>
          <v-list-item v-else v-bind:key="item.title">
            <v-list-tile avatar>
              <v-list-tile-avatar>
                <v-icon fa dark>{{ item.avatar }}</v-icon>
              </v-list-tile-avatar>
              <v-list-tile-content>
                <v-list-tile-title v-html="item.title"/>
                <v-list-tile-sub-title v-html="item.subtitle"/>
              </v-list-tile-content>
            </v-list-tile>
          </v-list-item>
        </template>
      </v-list>
    </v-card-text>
    <v-card-row actions>
      <v-btn flat class="">Subscribe</v-btn>
    </v-card-row>
  </v-card>

</template>
<script src="./slr-indicators.js"></script>
