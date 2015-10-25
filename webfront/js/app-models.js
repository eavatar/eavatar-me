
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
    initialize: function() {

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

