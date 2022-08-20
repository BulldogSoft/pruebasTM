odoo.define('bi_pos_import_sale.SODetail', function(require) {
	'use strict';

	const Registries = require('point_of_sale.Registries');
	const AbstractAwaitablePopup = require('point_of_sale.AbstractAwaitablePopup');

	class SODetail extends AbstractAwaitablePopup {
		constructor() {
			super(...arguments);
		}

		back() {
			this.trigger('close-popup');
		}

	}
	
	SODetail.template = 'SODetail';
	Registries.Component.add(SODetail);
	return SODetail;
});
