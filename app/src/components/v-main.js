import SlrIndicators from '@/components/SlrIndicators';

export default {
  name: 'v-main',
  data () {
    return {
      nav2: false,
      msg: 'Welcome to Your Vue.js App'
    };
  },
  components: {
    'slr-indicators': SlrIndicators
  }
};
