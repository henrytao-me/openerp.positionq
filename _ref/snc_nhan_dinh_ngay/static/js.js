openerp.snc_nhan_dinh_ngay = function (instance) {

var _t = instance.web._t;
var _lt = instance.web._lt;
var QWeb = instance.web.qweb;

$(window).bind('list.load_list', function(e, trigger){
	try{
		var view = trigger.view;
		var model = view.model;
		if(view.fields_view.arch.attrs.alias == 'snc_nhan_dinh_ngay'){
			var $buttons = view.options.$buttons;
			//snc_nhan_dinh_ngay_label			
			if(!$buttons.find('.snc_nhan_dinh_ngay_label').isExist()){
				$label = $('<span class="snc_nhan_dinh_ngay_label">');
				$buttons.append($label);
				//call
				var obj = new instance.web.Model('snc.nhan.dinh.ngay.setup');
				obj.call('get_state_info', []).then(function(data, status){
					$label.html(data.msg);
					if(data.status == true){
						$label.prepend($('<div style="margin-right:5px;display:inline-block;width:10px;height:10px;background-color:#339933">'));	
					}else{
						$label.prepend($('<div style="margin-right:5px;display:inline-block;width:10px;height:10px;background-color:#c81010">'));
					};
					
				});
			}			
		};	
	}catch(ex){};
});

};
