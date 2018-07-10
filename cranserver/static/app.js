// Vue for Top Bar to Fill Deployment Environment Label
var topbar = new Vue({
  el: '#app-environ',
  data: {
    cranversion: ""
  },
  methods: {
    getEnvironment: function() {
      this.$http.get('/environment').then(function(response){
        this.cranversion = response.data.replace(/['"]+/g, '');
      }, function(error){
        console.log(error.statusText);
      });
    }
  },
  mounted: function() {
    this.getEnvironment();
  }
})

// Vue Componenets for Main App
Vue.component('package-item', {
  props: ['package'],
    template: `
      <div class="panel panel-default">
        <div class="panel-heading">
          <h3 class="panel-title">{{ package.name }}</h3>
        </div>
        <ul class="list-group">
          <package-detail v-for="art in package.artifacts" v-bind:artifact="art"></package-detail>
        </ul>
      </div>`
})

Vue.component('package-detail', {
  props: ['artifact'],
    template: `
      <li class="list-group-item">
        <a v-bind:href="artifact.artifact_link">{{ artifact.version }} <em>({{ artifact.date }})</em></a>
      </li>`
})



// Vue for Main App
var app = new Vue({
  el: '#app',
  data: {
    packageList: [],
    filterText: ""
  },
  
  methods: {

    getPackages: function() {
      this.$http.get('/available').then(function(response){
        this.packageList = response.data;
      }, function(error){
        console.log(error.statusText);
      });
    },

    searchPackages: function(dataList) {
      return dataList.filter(val => val.name.match(this.filterText) !== null)
    }

  },

  mounted: function() {
    this.getPackages();
  }

})
