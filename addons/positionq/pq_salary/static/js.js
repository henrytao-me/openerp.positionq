openerp.pq_salary = function(instance) {

	var QWeb = instance.web.qweb;

	var www = {
		w1 : null,
		w2 : null,
		w3 : null
	};

	/*
	 * custom widget
	 */
	var template = instance.web.form.AbstractField.extend(instance.web.form.ReinitializeFieldMixin, {
		template : 'pq_salary_w1',
		_t : {
			table : '.custom'
		},
		data : null,
		id : null,
		flow : null,

		init : function() {
			this.flow = {
				readonly : true,
				loadData : false,
				renderData : true,
				commitData : true,
				committing : false,
				start : {
					load : false,
					commit : false
				}
			};
			this._super.apply(this, arguments);
		},

		get : function(key) {
			return key === 'readonly' ? false : this._super.apply(this, arguments);
		},

		get_t : function(key) {
			return this.template + this._t[key];
		},

		render_value : function() {
			var self = this;
			self._super.apply(self, arguments);
			// store id
			if (self.id !== self.view.dataset.ids[self.view.dataset.index]) {
				self.flow.loadData = false;
			};
			self.id = self.view.dataset.ids[self.view.dataset.index];
			// store state
			if (self.flow.readonly !== self.get('effective_readonly') && (self.get('effective_readonly') !== true || self.flow.readonly !== true)) {
				self.flow.renderData = false;
			};
			self.flow.readonly = self.get('effective_readonly');
			if (self.flow.readonly !== true) {
				self.flow.commitData = false;
			};
			// check init data
			if (self.flow.loadData !== true) {
				if (self.flow.start.load !== true) {
					self.flow.start.load = true;
					self.load_data();
				};
			} else {
				if (self.flow.renderData !== true) {
					self.render_data();
				};
			};
		},

		commit_value : function() {
			var self = this;
			self._super.apply(self, arguments);
			if (self.flow.commitData !== true) {
				self.committing = true;
				if (self.flow.start.commit !== true) {
					self.flow.start.commit = true;
					self.commit_data();
				};
			};
		},

		/*
		 * inherit this method
		 */

		load_data : function() {
			this.flow.loadData = true;
			this.flow.start.load = false;
			this.render_data();
		},

		render_data : function() {
			this.flow.renderData = true;
		},

		commit_data : function() {
			this.flow.commitData = true;
			this.flow.committing = false;
			this.flow.start.commit = false;
			this.load_data();
		}
	});

	/*
	 * pq_salary_w1
	 */

	instance.web.form.widgets.add('pq_salary_w1', 'instance.web.form.pq_salary_w1');
	instance.web.form.pq_salary_w1 = template.extend({
		template : 'pq_salary_w1',

		init : function() {
			this._super.apply(this, arguments);
			www.w1 = this;
		},

		load_data : function() {
			var self = this;
			var callback = (function(_super, args) {
				return function() {
					_super.apply(self, args);
				};
			})(self._super, arguments);
			// get data from server
			var model = new instance.web.Model('pq.nhom.vi.tri.yeu.to');
			model.call('get_yeu_to_matrix', [self.id]).then(function(res, status) {
				self.data = res;
				callback();
			});
		},

		render_data : function() {
			var self = this;
			// render template
			var $table = $(instance.web.qweb.render(self.get_t('table')));
			ngApp.controller(self.template, function($scope) {
				$scope.res = self.data;
				$scope.widget = self;
				$scope.check = function(a, b, formula) {
					if (formula == 'g') {
						return a > b;
					};
					if (formula == 'l') {
						return a < b;
					};
					if (formula == 'e') {
						return a == b;
					};
					return false;
				};
				$scope.percent = function(value) {
					return (parseInt(Math.round(value, 4) * 10000) / 100) + '%';
				}, $scope.bgcolor = function(val) {
					return self.get('effective_readonly') && value || val != true ? 'auto' : '#eeeeee';
				}
			});
			angular.bootstrap($table[0], ['ngApp']);
			self.$el.empty().append($table);
			// success
			self._super.apply(self, arguments);
		},

		commit_data : function() {
			var self = this;
			var callback = (function(_super, args) {
				return function() {
					_super.apply(self, args);
				};
			})(self._super, arguments);
			var model = new instance.web.Model('pq.nhom.vi.tri.yeu.to');
			model.call('set_yeu_to_matrix', [self.id, self.data.data]).then(function(res, status) {
				callback();
				www.w3.load_data();
			});
		}
	});

	/*
	 * pq_salary_w2
	 */

	instance.web.form.widgets.add('pq_salary_w2', 'instance.web.form.pq_salary_w2');
	instance.web.form.pq_salary_w2 = template.extend({
		template : 'pq_salary_w2',
		saved : true,

		init : function() {
			this._super.apply(this, arguments);
			www.w2 = this;
		},

		load_data : function() {
			var self = this;
			var callback = (function(_super, args) {
				return function() {
					_super.apply(self, args);
				};
			})(self._super, arguments);
			// get data from server
			var model = new instance.web.Model('pq.nhom.vi.tri.yeu.to');
			model.call('get_tieu_chi_matrix', [self.id]).then(function(res, status) {
				self.data = res;
				callback();
			});
		},

		render_data : function() {
			var self = this;
			// render template
			var $table = $(instance.web.qweb.render(self.get_t('table')));
			ngApp.controller(self.template, function($scope) {
				$scope.res = self.data;
				$scope.widget = self;
				$scope.percent = function(value) {
					return (parseInt(Math.round(value, 4) * 10000) / 100) + '%';
				}, $scope.length = function(obj) {
					var len = Object.keys(obj).length;
					return len == 0 ? 1 : len;
				}
			});
			angular.bootstrap($table[0], ['ngApp']);
			self.$el.empty().append($table);
			// success
			self._super.apply(self, arguments);
		},

		commit_data : function() {
			var self = this;
			var callback = (function(_super, args) {
				return function() {
					_super.apply(self, args);
				};
			})(self._super, arguments);
			var model = new instance.web.Model('pq.nhom.vi.tri.yeu.to');
			model.call('set_tieu_chi_matrix', [self.id, self.data]).then(function(res, status) {
				callback();
			});
		}
	});

	/*
	 * pq_salary_w3
	 */

	instance.web.form.widgets.add('pq_salary_w3', 'instance.web.form.pq_salary_w3');
	instance.web.form.pq_salary_w3 = template.extend({
		template : 'pq_salary_w3',
		saved : true,

		init : function() {
			this._super.apply(this, arguments);
			www.w3 = this;
		},

		load_data : function() {
			var self = this;
			var callback = (function(_super, args) {
				return function() {
					_super.apply(self, args);
				};
			})(self._super, arguments);
			// get data from server
			var model = new instance.web.Model('pq.nhom.vi.tri.yeu.to');
			model.call('get_tieu_chi_bac_matrix', [self.id]).then(function(res, status) {
				self.data = res;
				callback();
			});
		},

		render_data : function() {
			var self = this;
			// render template
			var $table = $(instance.web.qweb.render(self.get_t('table')));
			ngApp.controller(self.template, function($scope) {
				$scope.res = self.data;
				$scope.widget = self;
				$scope.percent = function(value) {
					return (parseInt(Math.round(value, 4) * 10000) / 100) + '%';
				};
				$scope.length = function(obj) {
					var len = Object.keys(obj).length;
					return len == 0 ? 1 : len;
				};
				$scope.bgcolor = function() {
					return self.get('effective_readonly') ? 'auto' : '#eeeeee';
				}
			});
			angular.bootstrap($table[0], ['ngApp']);
			self.$el.empty().append($table);
			// success
			self._super.apply(self, arguments);
		},

		commit_data : function() {
			var self = this;
			var callback = (function(_super, args) {
				return function() {
					_super.apply(self, args);
				};
			})(self._super, arguments);
			var model = new instance.web.Model('pq.nhom.vi.tri.yeu.to');
			model.call('set_tieu_chi_bac_matrix', [self.id, self.data]).then(function(res, status) {
				callback();
			});
		}
	});

	/*
	 *
	 * vi tri - yeu to
	 *
	 */

	instance.web.custom.widgets.add('vi_tri_yeu_to_diem', 'instance.web.custom.tmp.vi_tri_yeu_to_diem');
	instance.web.custom.tmp.vi_tri_yeu_to_diem = instance.web.Widget.extend({
		template : 'vi_tri_yeu_to_diem',
		parent : null,
		r : null,
		data : null,
		view_mode : true,

		init : function(parent, r) {
			this.parent = parent;
			this.r = r;
			this.init_ui();
			this.load_data();
			if (!$('.mybg').isExist()) {
				$('body').prepend($('<div class="mybg">'));
			};
		},

		get : function(key) {
			switch(key) {
				case 'effective_readonly':
					return this.view_mode;
					break;
			};
			return false;
		},

		init_ui : function() {
			var self = this;
			// init button
			var buttons = {
				edit : $('<button class="oe_button oe_form_button_save oe_highlight">Edit</button>'),
				save : $('<button class="oe_button oe_form_button_save oe_highlight">Save</button>'),
				discard : $('<a class="oe_bold oe_form_button_cancel" accesskey="D">Discard</a>')
			};
			var menubar = {
				view : $('<span class="oe_form_buttons_view">').append(buttons.edit),
				edit : $('<span class="oe_form_buttons_edit">').append(buttons.save).append($('<span class="oe_fade" style="margin-left:5px;margin-right:5px;">or</span>')).append(buttons.discard).hide()
			};
			this.parent.$el.parent().parent().parent().find('.oe_view_manager_buttons').append(menubar.view).append(menubar.edit);
			// button event
			buttons.edit.click(function(e) {
				menubar.view.hide();
				menubar.edit.show();
				// set view mode
				self.view_mode = false;
				self.render_data();
			});
			buttons.save.click(function(e) {
				menubar.view.show();
				menubar.edit.hide();
				// set view mode
				self.view_mode = true;
				self.commit_data();
			});
			buttons.discard.click(function(e) {
				menubar.view.show();
				menubar.edit.hide();
				// set view mode
				self.view_mode = true;
				self.render_data();
			});
		},

		load_data : function() {
			var self = this;
			// get data from server
			var model = new instance.web.Model('pq.vi.tri.yeu.to');
			model.call('get_matrix', []).then(function(res, status) {
				self.data = res;
				self.render_data();
			});
		},

		render_data : function() {
			var self = this;
			// render template
			var $table = $(instance.web.qweb.render(self.template, {
				res : self.data,
				widget : self
			}));
			ngApp.controller(self.template, function($scope) {
				$scope.res = self.data;
				$scope.widget = self;
				$scope.percent = function(value) {
					return (parseInt(Math.round(value, 4) * 10000) / 100) + '%';
				};
				$scope.length = function(obj) {
					var len = Object.keys(obj).length;
					return len == 0 ? 1 : len;
				};
				$scope.bgcolor = function() {
					return self.get('effective_readonly') ? 'auto' : '#eeeeee';
				};
			});
			angular.bootstrap($table[0], ['ngApp']);
			self.parent.$el.empty().append($table);
		},

		commit_data : function() {
			var self = this;
			var model = new instance.web.Model('pq.vi.tri.yeu.to');
			model.call('set_matrix', [self.data.matrix]).then(function(res, status) {
				self.load_data();
			});
		}
	});

	/*
	 *
	 * pt_ltt
	 *
	 */

	instance.web.custom.widgets.add('view_custom_pq_ltt', 'instance.web.custom.tmp.view_custom_pq_ltt');
	instance.web.custom.tmp.view_custom_pq_ltt = instance.web.Widget.extend({
		template : 'view_custom_pq_ltt',
		parent : null,
		r : null,
		data : null,

		init : function(parent, r) {
			this.parent = parent;
			this.r = r;
			this.init_ui();
			this.load_data();
		},

		get : function(key) {
			switch(key) {
				case 'effective_readonly':
					return this.view_mode;
					break;
			};
			return false;
		},

		init_ui : function() {
			var self = this;
		},

		load_data : function() {
			var self = this;
			// get data from server
			var model = new instance.web.Model('pq.ltt');
			model.call('get_data', []).then(function(res, status) {
				self.data = res;
				self.render_data();
			});
		},

		render_data : function() {
			var self = this;
			// render template
			var $table = $(instance.web.qweb.render(self.template, {
				res : self.data,
				widget : self
			}));
			self.parent.$el.empty().append($table);
		}
	});

	/*
	 *
	 * view_custom_pq_vi_tri_luong
	 *
	 */

	instance.web.custom.widgets.add('view_custom_pq_vi_tri_luong', 'instance.web.custom.tmp.view_custom_pq_vi_tri_luong');
	instance.web.custom.tmp.view_custom_pq_vi_tri_luong = instance.web.Widget.extend({
		template : 'view_custom_pq_vi_tri_luong',
		parent : null,
		r : null,
		data : null,
		view_mode : true,

		init : function(parent, r) {
			this.parent = parent;
			this.r = r;
			this.init_ui();
			this.load_data();
			if (!$('.mybg').isExist()) {
				$('body').prepend($('<div class="mybg">'));
			};
		},

		get : function(key) {
			switch(key) {
				case 'effective_readonly':
					return this.view_mode;
					break;
			};
			return false;
		},

		init_ui : function() {
			var self = this;
			// init button
			var buttons = {
				edit : $('<button class="oe_button oe_form_button_save oe_highlight">Edit</button>'),
				save : $('<button class="oe_button oe_form_button_save oe_highlight">Save</button>'),
				discard : $('<a class="oe_bold oe_form_button_cancel" accesskey="D">Discard</a>')
			};
			var menubar = {
				view : $('<span class="oe_form_buttons_view">').append(buttons.edit),
				edit : $('<span class="oe_form_buttons_edit">').append(buttons.save).append($('<span class="oe_fade" style="margin-left:5px;margin-right:5px;">or</span>')).append(buttons.discard).hide()
			};
			this.parent.$el.parent().parent().parent().find('.oe_view_manager_buttons').append(menubar.view).append(menubar.edit);
			// button event
			buttons.edit.click(function(e) {
				menubar.view.hide();
				menubar.edit.show();
				// set view mode
				self.view_mode = false;
				self.render_data();
			});
			buttons.save.click(function(e) {
				menubar.view.show();
				menubar.edit.hide();
				// set view mode
				self.view_mode = true;
				self.commit_data();
			});
			buttons.discard.click(function(e) {
				menubar.view.show();
				menubar.edit.hide();
				// set view mode
				self.view_mode = true;
				self.render_data();
			});
		},

		load_data : function() {
			var self = this;
			// get data from server
			var model = new instance.web.Model('pq.vi.tri');
			model.call('get_tong_ket_luong', []).then(function(res, status) {
				self.data = res;
				self.render_data();
			});
		},

		render_data : function() {
			var self = this;
			// render template
			var $table = $(instance.web.qweb.render(self.template, {
				res : self.data,
				widget : self,
				percent : function(value) {
					return (parseInt(value * 10000) / 100) + '%';
				},
				round : function(value) {
					return $.ekit.toFixed(value, 2) || 0;
				},
				format : function(value) {

				},
				bgColor: function() {
					return self.get('effective_readonly') ? 'auto' : '#eeeeee';
				}
			}));
			ngApp.controller(self.template, function($scope) {
				$scope.res = self.data;
				$scope.widget = self;
			});
			angular.bootstrap($table[0], ['ngApp']);
			self.parent.$el.empty().append($table);
		},

		commit_data : function() {
			var self = this;
			var model = new instance.web.Model('pq.vi.tri');
			model.call('set_tong_ket_luong', [self.data]).then(function(res, status) {
				self.load_data();
			});
		}
	});

	// instance.web.custom.widgets.add('view_custom_pq_vi_tri_luong', 'instance.web.custom.tmp.view_custom_pq_vi_tri_luong');
	// instance.web.custom.tmp.view_custom_pq_vi_tri_luong = instance.web.Widget.extend({
	// template: 'view_custom_pq_vi_tri_luong',
	// parent: null,
	// r: null,
	// data: null,
	//
	// init: function(parent, r) {
	// this.parent = parent;
	// this.r = r;
	// this.init_ui();
	// this.load_data();
	// },
	//
	// get: function(key){
	// switch(key){
	// case 'effective_readonly':
	// return this.view_mode;
	// break;
	// };
	// return false;
	// },
	//
	// init_ui: function(){
	// var self = this;
	// },
	//
	// load_data: function() {
	// var self = this;
	// // get data from server
	// var model = new instance.web.Model('pq.vi.tri');
	// model.call('get_tong_ket_luong', []).then(function(res, status) {
	// self.data = res;
	// self.render_data();
	// });
	// },
	//
	// render_data: function(){
	// var self = this;
	// // render template
	// var $table = $(instance.web.qweb.render(self.template, {
	// res: self.data,
	// widget: self,
	// percent: function(value) {
	// return (parseInt(value * 10000) / 100) + '%';
	// },
	// round: function(value){
	// return $.ekit.toFixed(value, 2) || 0;
	// },
	// format: function(value){
	//
	// }
	// }));
	// self.parent.$el.empty().append($table);
	// }
	// });

};
