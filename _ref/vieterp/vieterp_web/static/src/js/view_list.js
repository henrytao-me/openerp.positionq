/*---------------------------------------------------------
 * VietERP web_list
 * 1. fix: paging in sub list view
 * 2. fix: more pager option
 * 3. support: class="oe_view_only" class="oe_edit_only" in fields
 * 4. support: widget="group_by" hide_selector="true"
 * 5. support: widget="custom" 
 * 		list_template="xml_template_name"
 * 		list_data="py_model_function_name"
 * 		rows_template="xml_template_name"
 * 		rows_data="py_model_function_name"
 * 6. support: trigger "list.group_header.add"
 * 7. support: trigger "list.body.init"
 * 8. support: trigger "list.load_list"
 *---------------------------------------------------------*/

openerp.vieterp_web.view_list = function (instance) {
// var a = function (instance) {



var _t = instance.web._t;
var _lt = instance.web._lt;
var QWeb = instance.web.qweb;



var func_render_complete = function($el){
	try{
		var is_group_by = false;
		for(var i in $el.data('widget_group_by').group_by){
			if(!$el){
				continue;
			}
			$el.find('td[data-field="'+$el.data('widget_group_by').group_by[i]+'"]').hide();
			$el.find('th[data-id="'+$el.data('widget_group_by').group_by[i]+'"]').hide();
			is_group_by = true;
		}
		if($el.data('widget_group_by').hide_selector === 'true' && is_group_by === true){
			$el.find('input.oe_list_record_selector[type="checkbox"]').parent().hide();
			$el.find('th.oe_list_record_selector').hide();
			var is_hide = false;
			$el.find('tfoot tr td').each(function(){
				if($(this).attr('data-field') === undefined && is_hide === false){
					$(this).hide();
					$(this).css('display', 'none !important');
					is_hide = true;
				}
			})
		}	
	}catch(ex){};
};



instance.web.ListView.include({
	init: function(){
		var self = this;
		this._super.apply(this, arguments);

		this.__is_limit = false;
		this.__is_pager = false;
	},
	limit: function(){
		var self = this;
		this._super.apply(this, arguments);
		
		if(this.__is_limit !== true){
			this.__is_limit = true;
			this._limit = (this.options.limit
	                    || this.defaults.limit
	                    || (this.getParent().action || {}).limit
	                    || 10);	
		}
        return this._limit;
	},	
	ex_set_pager: function(){
		var self = this;
		if(this.__is_pager !== true){
			this.__is_pager = true;
			this.$pager.find('.oe_list_pager_state')
				.click(function (e) {
                        e.stopPropagation();
                        var $this = $(this);

                        var $select = $('<select>')
                            .appendTo($this.empty())
                            .click(function (e) {e.stopPropagation();})
                            .append('<option value="10">10</option>' +
                            		'<option value="20">20</option>' +
                            		'<option value="50">50</option>' +
                            		'<option value="80">80</option>' +                            		
                                    '<option value="100">100</option>' +
                                    '<option value="200">200</option>' +
                                    '<option value="500">500</option>' +
                                    '<option value="NaN">' + _t("Unlimited") + '</option>')
                            .change(function () {
                                var val = parseInt($select.val(), 10);
                                self._limit = (isNaN(val) ? null : val);
                                self.page = 0;
                                self.reload_content();
                            }).blur(function() {
                                $(this).trigger('change');
                            })                       
                            .val(self._limit || 'NaN');
                    });
		};
	},
	load_list: function(data){
		var args = arguments;				
		//init callback
		var _template = this._template;
		var callback = function(){
			this._super.apply(this, args);
			this._template = _template;
		};
		callback.call(this);
		//
		var widget = this.fields_view.arch.attrs['widget'] || '';
		if(widget.replace(" ", "").split(',').indexOf('custom') >= 0){
			var widget_custom = {
				_list_template: this.fields_view.arch.attrs['list_template'],
				_list_data: this.fields_view.arch.attrs['list_data'],
				_rows_template: this.fields_view.arch.attrs['rows_template'],
				_rows_data: this.fields_view.arch.attrs['rows_data'],
				_model: this.model
			};
			this.widget_custom = widget_custom;
			//list_template
			if(widget_custom._list_template){
				this._template = widget_custom._list_template;	
			};
			//list_data			
			if(widget_custom._list_data){
				var model = new instance.web.Model(widget_custom._model);
				var self = this;
				model.call(widget_custom._list_data, [self.$el.data('domain'), self.$el.data('context')]).then(function(data, status){
	    			self.widget_custom.list_data = data;
	    			//
	    			self.$el.children('table').children().not('tbody').remove();
	    			self.$el.children('table').append($(QWeb.render(self._template, self)).html());			
	    		});
			};
		};
		//buttons
		var buttons = this.fields_view.arch.attrs['buttons'] || false;
		if(buttons){			
			if(!this.$buttons.find('.custom_buttons').isExist()){
				var $custom_buttons = $('<span class="custom_buttons">');
				this.$buttons.append($custom_buttons);				
				buttons = buttons.replaceAll("'", '"');			
				buttons = JSON.parse(buttons);
				//
				for(var i in buttons){
					$button = $('<button>');
					$button.html(buttons[i]['string'] || '...');
					$button.addClass(buttons[i]['class'] || '');
					$button.data('name', i);
					$button.data('attrs', buttons[i]);
					$button.click(function(){
						
					});
					$custom_buttons.append($button);	
				};
			};		
		};
		
		//finallize
		this.ex_set_pager();
		//trigger
		$(window).trigger('list.load_list', [{view: this, $this: this.$el}]);  
	},
	do_search: function (domain, context, group_by) {			
		var self = this;
		var widget = this.fields_view.arch.attrs['widget'] || '';		
		if(widget.replace(" ", "").split(',').indexOf('group_by') >= 0){
			if(group_by){
				this.$el.data('widget_group_by', {
					group_by: group_by,
					hide_selector: this.fields_view.arch.attrs.hide_selector
				});
			}else{
				this.$el.data('widget_group_by', {
					group_by: [],
					hide_selector: false
				});
			};
		};
		this.$el.data('context', context);
		this.$el.data('group_by', group_by);
		this._super(domain, context, group_by);
	}
});



instance.web.ListView.List.include({
	init: function (group, opts) {
		var self = this;
		this._super.apply(this, arguments);
		this.record_callbacks['change'] = function (event, record, attribute, value, old_value) {
            var $row;
            if (attribute === 'id') {
                if (old_value) {
                    throw new Error(_.str.sprintf( _t("Setting 'id' attribute on existing record %s"),
                        JSON.stringify(record.attributes) ));
                }
                if (!_.contains(self.dataset.ids, value)) {
                    // add record to dataset if not already in (added by
                    // the form view?)
                    self.dataset.ids.splice(
                        self.records.indexOf(record), 0, value);
                }
                // Set id on new record
                $row = self.$current.children('[data-id=false]');
            } else {
                $row = self.$current.children(
                    '[data-id=' + record.get('id') + ']');
            }
            $row.replaceWith(self.render_record(record));
            func_render_complete(self.view.$el);            
        };
        
        this.records.unbind('change');
        this.records.bind('change', this.record_callbacks['change']);
        
        //
        $(window).trigger('list.body.init', [{$body: this.$current, 
        	                                           $el: self.view.$el, 
        	                                           view: self.view}]);     
	},
	pad_table_to: function(count){		
		if(this.view.grouped == true){
			return;
		}
		//		
		var self = this;
		try{
			var row = 0;
			this.view.$el.children('table').children('thead').children('tr').first().children().each(function(e){
				var colspan = 1;
				if($(this).attr('colspan')){
					colspan = parseInt($(this).attr('colspan'));
				};
				row += colspan;
			});
			if(row == 0){
				this._super.apply(this, arguments);
			}else{
				row = '<tr class="pad_table_to"><td colspan="'+row+'"></td></tr>';
				records_length = this.records.length;
				try{					
					if(this.view.widget_custom){
						records_length = this.view.widget_custom.rows_data.length;
					};		
					
				}catch(ex){};
				// this.$current
		            // .children('tr:not([data-id])').remove().end()
		            // .append(new Array(count - records_length + 1).join(row));
		        if(count - records_length + 1 > 0){
		        	this.$current
		        		.children('tr.pad_table_to').remove().end()
		            	.append(new Array(count - records_length + 1).join(row));	
		        };
			};				        
		}catch(ex){
			this._super.apply(this, arguments);	
		};
	},	
	render_record: function (record) {
		var self = this;
        var index = this.records.indexOf(record);
        //
        var row_template = 'ListView.row';
        var widget_custom = this.view.widget_custom;
        if(widget_custom){
        	if(widget_custom._rows_template){
        		row_template = widget_custom._rows_template.slice(0, -1);        		 
        	}
        }
        //
        var res = QWeb.render(row_template, {
            columns: this.columns,
            options: this.options,
            record: record,
            row_parity: (index % 2 === 0) ? 'even' : 'odd',
            view: this.view,
            render_cell: function () {            	
                return self.render_cell.apply(self, arguments);
            }
        });
        //
        res = $(res);        
		func_render_complete(this.view.$el);
        //
        return res;
	},
	render: function () {
		var rows_template = 'ListView.rows';
		var rows_data = _.extend({
            render_cell: function () {
                return self.render_cell.apply(self, arguments); }
        }, this);
        //init callback
        var callback = function(){        	
	        this.$current.empty().append(QWeb.render(rows_template, rows_data));
	        this.pad_table_to(4); 
        };
        //
        var widget_custom = this.view.widget_custom;
        if(widget_custom){
			if(widget_custom._rows_template){
				rows_template = widget_custom._rows_template;
			};
			if(widget_custom._rows_data){
				var model = new instance.web.Model(widget_custom._model);
				var self = this;
				model.call(widget_custom._rows_data, [this.view.$el.data('domain'), this.view.$el.data('context')]).then(function(data, status){
	    			self.view.widget_custom.rows_data = data;	    			
	    			rows_data.widget_custom = self.view.widget_custom;
	    			callback.call(self);	    						
	    		});
			}else{
				callback.call(this);
			};
        }else{
        	this._super.apply(this, arguments);
        };
		//
    },
});



instance.web.ListView.Groups.include({
	render: function (post_render) {
        var self = this;
        var $el = $('<tbody>');
        this.elements = [$el[0]];

        this.datagroup.list(
            _(this.view.visible_columns).chain()
                .filter(function (column) { return column.tag === 'field' })
                .pluck('name').value(),
            function (groups) {
                $el[0].appendChild(
                    self.render_groups(groups));
                if (post_render) { post_render(); }
            }, function (dataset) {
            	var success = function(filter_ids){
	            	self.render_dataset(dataset, filter_ids).done(function (list) {
	                    self.children[null] = list;
	                    self.elements =
	                        [list.$current.replaceAll($el)[0]];
	                    self.setup_resequence_rows(list, dataset);
	                    if (post_render) { post_render(); }
	                    self.render_completed();
	                });	
            	};
            	//ekit filter
            	var filter = self.view.options.filter;
            	if(filter){
            		try{
	            		filter = filter.replaceAll('(', '[')
	            						.replaceAll(')', ']')
	            						.replaceAll('TRUE', 'true')
	            						.replaceAll('True', 'true')
	            						.replaceAll('FALSE', 'false')
	            						.replaceAll('False', 'false')
	            						.replaceAll("'", '"');
	            		filter = JSON.parse(filter);
	            		var obj = new instance.web.Model(dataset.model);
						obj.call('search', [filter]).then(function(data, status){
							success(data);	
						});	
            		}catch(ex){
            			success();
            		};
            	}else{
            		success();
            	}
            });
        return $el;
    },
	// render: function (post_render) {
		// var self = this;			
		// var res = this._super(function(){
			// if(post_render){
				// post_render();	
			// }
			// self.render_completed();
		// });			
		// return res;
	// },
	render_completed: function(){
		func_render_complete(this.view.$el);
	},
	render_groups: function (datagroups) {
        var self = this;
        var placeholder = this.make_fragment();
        _(datagroups).each(function (group) {
            if (self.children[group.value]) {
                self.records.proxy(group.value).reset();
                delete self.children[group.value];
            }
            var child = self.children[group.value] = new (self.view.options.GroupsType)(self.view, {
                records: self.records.proxy(group.value),
                options: self.options,
                columns: self.columns
            });
            self.bind_child_events(child);
            child.datagroup = group;

            var $row = child.$row = $('<tr class="oe_group_header">');
            if (group.openable && group.length) {
                $row.click(function (e) {
                    if (!$row.data('open')) {
                        $row.data('open', true)
                            .find('span.ui-icon')
                                .removeClass('ui-icon-triangle-1-e')
                                .addClass('ui-icon-triangle-1-s');
                        child.open(self.point_insertion(e.currentTarget));
                    } else {
                        $row.removeData('open')
                            .find('span.ui-icon')
                                .removeClass('ui-icon-triangle-1-s')
                                .addClass('ui-icon-triangle-1-e');
                        child.close();
                    }
                });
            }
            
            placeholder.appendChild($row[0]);

            var $group_column = $('<th class="oe_list_group_name">').appendTo($row);
            // Don't fill this if group_by_no_leaf but no group_by
            if (group.grouped_on) {
                var row_data = {};
                row_data[group.grouped_on] = group;
                var group_column = _(self.columns).detect(function (column) {
                    return column.id === group.grouped_on; });
                if (! group_column) {
                    throw new Error(_.str.sprintf(
                        _t("Grouping on field '%s' is not possible because that field does not appear in the list view."),
                        group.grouped_on));
                }
                var group_label;
                try {
                    group_label = group_column.format(row_data, {
                        value_if_empty: _t("Undefined"),
                        process_modifiers: false
                    });
                } catch (e) {
                    group_label = _.str.escapeHTML(row_data[group_column.id].value);
                }
                // group_label is html-clean (through format or explicit
                // escaping if format failed), can inject straight into HTML
                $group_column.html(_.str.sprintf(_t("%s (%d)"),
                    group_label, group.length));

                if (group.length && group.openable) {
                    // Make openable if not terminal group & group_by_no_leaf
                    $group_column.prepend('<span class="ui-icon ui-icon-triangle-1-e" style="float: left;">');
                } else {
                    // Kinda-ugly hack: jquery-ui has no "empty" icon, so set
                    // wonky background position to ensure nothing is displayed
                    // there but the rest of the behavior is ui-icon's
                    $group_column.prepend('<span class="ui-icon" style="float: left; background-position: 150px 150px">');
                }
            }
            self.indent($group_column, group.level);

            if (self.options.selectable) {
                $row.append('<th class="oe_list_record_selector">');                
            }
            _(self.columns).chain()
                .filter(function (column) { return column.invisible !== '1'; })
                .each(function (column) {
                    if (column.meta) {
                        // do not do anything
                    } else if (column.id in group.aggregates) {
                        var r = {};
                        r[column.id] = {value: group.aggregates[column.id]};
                        $('<td class="oe_number '+column.class+'">')
                            .html(column.format(r, {process_modifiers: false}))
                            .appendTo($row);
                    } else {
                    	//ekit_upgrade
                        $row.append('<td data-field="'+column.id+'">');
                        //ekit_end
                    }
                });
            if (self.options.deletable) {
                $row.append('<td class="oe_list_group_pagination">');
            }
            
            //ekit_trigger
            $(window).trigger('list.group_header.add', [{$row: $row, 
            													  group: group, 
            													  $el: self.view.$el, 
            													  view: self.view}]);
        });
        return placeholder;
    },
    make_paginator: function () {
        var self = this;
        this._super.apply(this, arguments);
        //ekit        
        this.view.$el.find('.oe_list_group_pagination').children('button').addClass('oe_i');
        this.view.$el.find('.oe_list_group_pagination').children('button[data-pager-action="previous"]').html('(');
        this.view.$el.find('.oe_list_group_pagination').children('button[data-pager-action="next"]').html(')');
        //
        this.view.$el.find('.oe_list_group_pagination').wrapInner('<div style="display:none"/>');
    },
    render_dataset: function (dataset, filter_ids) {
    	var _ids = dataset.ids || [];
    	if(filter_ids){
    		tmp = []
    		for(var i = 0; i < _ids.length; i++){
    			if($.inArray(_ids[i], filter_ids) >= 0){
    				tmp.push(_ids[i]);
    			};
    		};
    		if(dataset.set_ids){
    			dataset.set_ids(tmp);
    		};
    	};
    	//
        var self = this,
            list = new (this.view.options.ListType)(this, {
                options: this.options,
                columns: this.columns,
                dataset: dataset,
                records: this.records
            });
        this.bind_child_events(list);

        var view = this.view,
           limit = view.limit(),
               d = new $.Deferred(),
            page = this.datagroup.openable ? this.page : view.page;

        var fields = _.pluck(_.select(this.columns, function(x) {return x.tag == "field"}), 'name');
        var options = { offset: page * limit, limit: limit, context: {bin_size: true} };
        //TODO xmo: investigate why we need to put the setTimeout
        $.async_when().done(function() {
            dataset.read_slice(fields, options).done(function (records) {
            	//
            	if(dataset.set_ids){
	    			dataset.set_ids(_ids);	
	    		};
                // FIXME: ignominious hacks, parents (aka form view) should not send two ListView#reload_content concurrently
                if (self.records.length) {
                    self.records.reset(null, {silent: true});
                }
                if (!self.datagroup.openable) {
                    view.configure_pager(dataset);
                } else {
                    if (dataset.size() == records.length) {
                        // only one page
                        self.$row.find('td.oe_list_group_pagination').empty();
                    } else {      
                    	//ekit
                    	self.$row.find('td.oe_list_group_pagination').children().show();
                    	//              	
                        var pages = Math.ceil(dataset.size() / limit);
                        self.$row
                            .find('.oe_list_pager_state')
                                .text(_.str.sprintf(_t("%(page)d/%(page_count)d"), {
                                    page: page + 1,
                                    page_count: pages
                                }))
                            .end()
                            .find('button[data-pager-action=previous]')
                                .css('visibility',
                                     page === 0 ? 'hidden' : '')
                            .end()
                            .find('button[data-pager-action=next]')
                                .css('visibility',
                                     page === pages - 1 ? 'hidden' : '');
                    }
                }

                self.records.add(records, {silent: true});
                list.render();
                d.resolve(list);
                if (_.isEmpty(records)) {
                    view.no_result();
                }
            });
        });
        return d.promise();
    },
});

};
