import Vue from 'vue';
import Router from 'vue-router';
import VMain from '@/components/VMain';
import VMap from '@/components/VMap';
import VStation from '@/components/VStation';

Vue.use(Router);

export default new Router({
  routes: [
    {
      path: '/',
      name: 'Main',
      component: VMain
    },
    {
      path: '/stations/:id',
      component: VStation
    }
  ]
});
