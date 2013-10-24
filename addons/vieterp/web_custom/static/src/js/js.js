/*---------------------------------------------------------
 * VietERP web_custom
 * Usage:
 * 1. trigger: view_custom.reloaded
 *---------------------------------------------------------*/

openerp.web_custom = function(instance) {

	var _t = instance.web._t;
	var _lt = instance.web._lt;
	var QWeb = instance.web.qweb;

	/*
	 * Widget Class
	 */

	var Widget = instance.web.Class.extend({
		data: {},

		add: function(key, value) {
			this.data[key] = value;
		},

		get: function(key) {
			return this.data[key];
		}
	});

	/*
	 * instance.web.custom
	 */

	instance.web.custom = {
		widgets: new Widget(),
		tmp: {}
	};

	/*
	 * view custom
	 */

	instance.web.views.add('custom', 'instance.web_custom.view');
	instance.web_custom.view = instance.web.View.extend({
		template: "CustomView",
		display_name: _lt('List'),
		view_type: 'custom',

		init: function(parent, dataset, view_id, options) {
			this._super.apply(this, arguments);
		},

		load_custom_view: function(r) {
			// get widget
			var widget = instance.web.custom.widgets.get(r.arch.attrs.widget);
			if(widget) {
				try {
					widget = eval(widget);
					widget = new widget(this, r);
				} catch(ex) {
				};
			};
		},

		view_loading: function(r) {
			this._super.apply(this, arguments);
			return this.load_custom_view(r);
		},

		destroy: function() {
			return this._super.apply(this, arguments);
		},

		do_search: function(domain, context, group_by) {
			return this._super.apply(this, arguments);
		},

		do_show: function() {
			this.do_push_state({});
			return this._super.apply(this, arguments);
		},
	});
};
