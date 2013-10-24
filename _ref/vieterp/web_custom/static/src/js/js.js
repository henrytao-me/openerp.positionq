/*---------------------------------------------------------
 * VietERP web_custom
 * Usage:
 * 1. trigger: view_custom.reloaded
 *---------------------------------------------------------*/

var toFixed = function(num, digits){
	if(digits == undefined || digits == null){
		digits = 2;
	};
	if(num == undefined || num == null || num == ''){
		return '';
	};
	return num.toFixed(digits);
}

openerp.web_custom = function (instance) {

var _t = instance.web._t;
var _lt = instance.web._lt;
var QWeb = instance.web.qweb;

instance.web.views.add('custom', 'instance.web_custom.view');
instance.web_custom.view = instance.web.View.extend({
    template: "CustomView",
    display_name: _lt('Custom'),
    view_type: "custom",
    _model: null,

    init: function(parent, dataset, view_id, options) {
        var self = this;
        this._super(parent);
        this.set_default_options(options);
        this.dataset = dataset;
        this.view_id = view_id;
        this._model = new instance.web.Model(this.dataset.model);
    },

    view_loading: function(r) {
        return this.load_custom_view(r);
    },

    destroy: function () {
        this._super();
    },

    load_custom_view: function(fields_view_get) {
        // TODO: move  to load_view and document
        var self = this;
        this.fields_view = fields_view_get;
        //get template info
        var template_name = this.fields_view.arch.attrs.template_name;
        var template_data = this.fields_view.arch.attrs.template_data;
        //get list action
        var actions = [];
        var action_full = [];        
        for(var i in this.fields_view.arch.children){
        	if(this.fields_view.arch.children[i].tag != 'action'){
        		continue;
        	};
        	actions.push(this.fields_view.arch.children[i].attrs);
        	action_full.push(this.fields_view.arch.children[i]);
        };
        //get data from template_data
		var self = this;
		var callback = function(data){
			var $this = $(QWeb.render(template_name, {
				template_data: data,
				action: actions,
				toFixed: toFixed			
			}));
			this.$el.empty().append($this);
			//get and append action data			
			for(var i in action_full){
				this.on_get_action(action_full[i]);			
			}
			//trigger			
			$(window).trigger('view_custom.reloaded', [{view: self, data: data, $this: $this}]);
		}; 
		if(template_data){
			self._model.call(template_data, [this.domain, this.context]).then(function(data, status){
				callback.call(self, data);		
			});
		}else{
			callback.call(self, {});
		};
    },
    
    on_get_action: function(action){
    	var self = this;
    	var action_id = _.str.toNumber(action.attrs.name);
        if (!_.isNaN(action_id)) {
            self.rpc('/web/action/load', {action_id: action_id}).done(function(result) {            	
                self.on_load_action(result, action.attrs);
            });
        };
    },
    
    on_load_action: function(result, action_attrs) {
        var self = this,
            action = result;            

        // evaluate action_attrs context and domain
        action_attrs.context = instance.web.pyeval.eval(
            'context', action_attrs.context || {});
        action_attrs.domain = instance.web.pyeval.eval(
            'domain', action_attrs.domain || [], action_attrs.context);
        
        if (action_attrs.context['custom_merge_domains_contexts'] === false) {
            // TODO: replace this 6.1 workaround by attribute on <action/>
            action.context = action_attrs.context || {};
            action.domain = action_attrs.domain || [];
        } else {
            action.context = instance.web.pyeval.eval(
                'contexts', [action.context || {}, action_attrs.context, this.context || {}]);
            action.domain = instance.web.pyeval.eval(
                'domains', [action_attrs.domain, action.domain || [], this.domain || []],
                action.context)
        }
        
        action.flags = {
            search_view : false,
            sidebar : false,
            views_switcher : false,
            action_buttons : false,
            pager: false,
            low_profile: true,
            display_title: false,
            list: {
                selectable: false
            }
        };
        
        var am = new instance.web.ActionManager(this),            
            $action = this.$el.find('*[action-id="'+action_attrs.id+'"]');
        // $action.parent().data('action_attrs', action_attrs);
        // this.action_managers.push(am);
        $action.empty();
        am.appendTo($action);
        am.do_action(action);
        // am.do_action = function (action) {
            // self.do_action(action);
        // };
    },
    
    do_search: function(domain, context, group_by) {
        this.domain = domain;
        this.context = context;
        this.group_by = group_by;
        //call load view
        this.load_custom_view(this.fields_view);
    },
    
    do_show: function() {
        this.do_push_state({});
        return this._super();
    },
});
};
