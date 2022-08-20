odoo.define('pos_document_type_bds.doctype', function(require) {
"use strict";

var models = require('point_of_sale.models');
const Registries = require('point_of_sale.Registries');
const PaymentScreen = require('point_of_sale.PaymentScreen');
const PosComponent = require('point_of_sale.PosComponent');
var _super_posmodel = models.PosModel.prototype;


models.load_models({
model: 'pos.config',
fields:['doctype_id'],
loaded: function(self,types){
	self.types=[];
	for(var i=0; i < types.length; i++){
		self.types.push(types[i]);
		}
	},
});

models.load_models({
model: 'pos.doc.type',
domain: function(self){return [['id', '=', self.config.doctype_id]]; },
loaded: function(self,vals){
	self.vals=[];
	for(var j=0; j < vals.length; j++){
		self.vals.push(vals[j]);
		}
	},
});


});