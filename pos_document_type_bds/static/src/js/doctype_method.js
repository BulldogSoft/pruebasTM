odoo.define('pos_document_type_bds.DocTypeMethod', function(require) {
	'use strict';

	const PosComponent = require('point_of_sale.PosComponent');
	const Registries = require('point_of_sale.Registries');
	const { useListener } = require('web.custom_hooks');
	var core = require('web.core');
	var QWeb = core.qweb;

	class DoctypeButton extends PosComponent {
		constructor() {
			super(...arguments);
			useListener('new-doctype-line', this.addNewdoctypeLine);
			console.log("TEST======")
		}
		addNewdoctypeLine(doctype){
			var order = this.env.pos.get_order();
			order['doctype_id'] = doctype['detail'].id
		}

		click_set_doctype(event){
			var self = this
			var on = parseInt(event.currentTarget.dataset['productId'])
			if(on){
				event.currentTarget[$('.doctype-name').css({'background-color': '#e2e2e2','color': '#666'})]
				event.currentTarget[$('#'+on).val(on).css({'background-color': '#875A7B','color':'#FFFFFF'})]
			}
		}
	}

	DoctypeButton.template = 'DoctypeButton';

	Registries.Component.add(DoctypeButton);

	return DoctypeButton;
});