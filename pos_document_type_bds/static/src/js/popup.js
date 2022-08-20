odoo.define('pos_document_type_bds.PaymentScreen', function(require) {
	"use strict";

	const Registries = require('point_of_sale.Registries');
	const PaymentScreen = require('point_of_sale.PaymentScreen');

	const DoctypepopupPaymentScreen = (PaymentScreen) =>
		class extends PaymentScreen {
			constructor() {
				super(...arguments);
			}

		async _finalizeValidation() {
			let self = this;
			if(this.currentOrder['doctype_id']){
				super._finalizeValidation();
			}else{
				self.showPopup('ConfirmPopup', {
					title: self.env._t('Selecionar Tipo de Documento'),
					body: self.env._t('Porfavor seleccionar un tipo de documentos antes de validar la orden'),
				});
			}
		}
	};

	Registries.Component.extend(PaymentScreen, DoctypepopupPaymentScreen);

	return PaymentScreen;

});