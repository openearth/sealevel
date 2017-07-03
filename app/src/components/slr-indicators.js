import 'font-awesome/css/font-awesome.min.css';
export default {
  name: 'slr-indicators',
  data () {
    return {
      indicators: [
        {
          avatar: 'snowflake-o',
          title: 'Ice melting',
          subtitle: 'Current sea-level rise due to ice melting'
        },
        {
          avatar: 'tint',
          title: 'Sea-level rise',
          subtitle: 'Current sea-level rise measured by tide gauges'

        }
      ]
    };
  }
};
