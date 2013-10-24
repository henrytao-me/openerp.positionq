$(function(){	
	$(window).bind('view_custom.reloaded', function(e, trigger) {
		var view = trigger.view;
		var data = trigger.data;
		var $this = trigger.$this;
		var _model = view._model;
		var listDatas = {};
		
		if (!$this.is('.lme_trading_custom')) {
			return;
		};
		
		var funcGetData = function(view, data){
			listDatas = {};
			_model.call('lme_trading_custom_load', []).then(function(datas, status){
				listDatas = datas;
				func(view, data);
			});
		}
		
		var funcSave = function(ngay, lmeClose, nonPromptsLme, isThirdWednesday, $dialog){
			//Build dict data send to server
			var dataSend = {}
			dataSend = {
				'ngay' : ngay,
				'is_third_wednesday' : isThirdWednesday,
				'lme_close' : lmeClose,
				'non_prompts_lme' : nonPromptsLme
			};
			//Save data to server
			_model.call('lme_trading_custom_save', [dataSend]).then(function(datas, status){
				//Remove if ngay existed in listDatas
				listDatas = $.grep(listDatas, function(value) {
					  return value['ngay'] != ngay;
				});
				//Append new ngay to listDatas
				listDatas.push(dataSend);
				$dialog.dialog("close");	
				$this.datepicker("refresh");
			});
		}
		
		var hightlightRangeOfDays = function(dd) {
			//format date value of datepicker when click on date
			var d = $.datepicker.formatDate('yy-mm-dd', dd);
			
			for (var i=0; i<listDatas.length; i++){
				//Get data
				var getDate = listDatas[i]['ngay'];
				var getLmeClose = listDatas[i]['lme_close'];
				var getIsThirdWednesday = listDatas[i]['is_third_wednesday'];
				var getNonPromptsLme = listDatas[i]['non_prompts_lme'];
				//Handle hightlight date
				if(d == getDate){
					if ((getLmeClose == true) && (getIsThirdWednesday == true) && (getNonPromptsLme == true)){
						return [true, 'lme-trading-three-type', 'LME Close - Non Prompts LME - Third Wednesday'];
					}
					if ((getLmeClose == true) && (getIsThirdWednesday == true)){
						return [true, 'lme-trading-tw-x', 'LME Close - Third Wednesday'];
					}
					if ((getIsThirdWednesday == true) && (getNonPromptsLme == true)){
						return [true, 'lme-trading-tw-o', 'Non prompts LME - Third Wednesday'];
					}
					if ((getLmeClose == true) && (getNonPromptsLme == true)){
						return [true, 'lme-trading-o-x', 'LME Close - Non Prompts LME'];
					}
					if (getLmeClose == true){
						return [true, 'lme-trading-close', 'LME Close'];
					}
					if (getNonPromptsLme == true){
						return [true, 'lme-trading-non-prompts', 'Non prompts LME'];
					}
					if (getIsThirdWednesday == true){
						return [true, 'lme-trading-third-webnesday', 'Third Wednesday'];
					}
				}
			}
			return [true];	
		}
		
		var func = function(view, data) {
			$this.datepicker({
				numberOfMonths : 12,
				showOtherMonths : true,
				dateFormat : 'yy-mm-dd',
				changeMonth : true,
				changeYear : true,
				beforeShowDay: hightlightRangeOfDays,
				onSelect : function(dateValue, inst) {
					
					////Set default value for components will show on dialog
					$('#lme-trading-date').val(dateValue);	
					var check = true;
					for (var i=0; i<listDatas.length; i++){
						var getDate = listDatas[i]['ngay'];
						if (dateValue == getDate){
							check = false;
							$('#lme-close').prop('checked', listDatas[i]['lme_close']);
							$('#non-prompts-lme').prop('checked', listDatas[i]['non_prompts_lme']);
							$('#third-wednesday').prop('checked', listDatas[i]['is_third_wednesday']);
						}
					}
					if (check == true){
						$('#lme-close').prop('checked', false);
						$('#non-prompts-lme').prop('checked', false);
						$('#third-wednesday').prop('checked', false);
					}
					
					//Show dialog allow user choose type of date
					$('#lme_trading_custom_dialog').dialog({
						title : "Vui lòng chọn loại",
						modal : true,
						bgiframe : true,
						width : '300px',
						resizable : false,
						show : 'fadein',
						hide : 'drop',
						buttons : [ {
								text : function() {
									return 'SAVE';
								},
								click : function(data) {
									var ngay = $('#lme-trading-date').val();
									var isThirdWednesday = $('#third-wednesday').is(':checked') ? true : false;
									var lmeClose = $('#lme-close').is(':checked') ? true : false;
									var nonPromptsLme = $('#non-prompts-lme').is(':checked') ? true : false;
									var $dialog = $(this);
									funcSave(ngay, lmeClose, nonPromptsLme, isThirdWednesday, $dialog);
								}
							}, {
								text : function() {
									return 'Cancel';
								},
								click : function(data) {
									$(this).dialog("close");
								}
							}, 
						],						
					});
				},
			});
	
		};
		funcGetData(view, data);		
	});
});
