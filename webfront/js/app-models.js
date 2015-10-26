
ava.models.Notice = Backbone.Model.extend({
    defaults: {
        kind: 'info',
        message: '',
        title: 'Ava Message'
    },

    initialize: function(){
    }
});


ava.models.Job = Backbone.Model.extend({
    initialize: function() {

    }
});


ava.models.Log = Backbone.Model.extend({

    defaults: {
        ts: 0,
        lvl: 20,
        lvl_name: 'INFO',
        msg: 'aa'
    },

    initialize: function(entry) {
        console.log('Log.initialize')
        console.log("    ts=", entry.ts, ",lvl=", entry.lvl, ',msg=', entry.msg)
        this.set('ts', entry.ts)
        this.set('lvl', entry.lvl)
        this.set('msg', entry.msg)
        if(entry.lvl < 30) {
            this.set('lvl_name', 'INFO')
        } else if(entry.lvl < 40) {
            this.set('lvl_name', 'ALERT')
        } else {
            this.set('lvl_name', 'ERROR')
        }

    }
});

ava.models.Logs = Backbone.Collection.extend({
    model: ava.models.Log,
    url: '/api/logs',
    parse: function(response){
        console.log("parse logs response")
        return response.data;
    }
});




ava.models.Script = Backbone.Model.extend({
    initialize: function() {
        this.title = ''
        this.content = ''
    }
});

ava.models.Scripts = Backbone.Collection.extend({
    model: ava.models.Script,

    initialize: function() {
    }
});

