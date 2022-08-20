// bi_pos_import_sale js
odoo.define('bi_pos_import_sale.models', function(require) {
	"use strict";

	var models = require('point_of_sale.models');
	var PosDB = require("point_of_sale.DB");

	var _super_order = models.Order.prototype;
	models.Order = models.Order.extend({
		initialize: function(attr, options) {
			this.imported_sales = this.imported_sales || [];
			_super_order.initialize.call(this,attr,options);
		},

		set_imported_sales: function(so){
			let sale = so.toString();
			if(!this.imported_sales.includes(sale))
				this.imported_sales += sale+',';
		},

		get_imported_sales: function(){
			return this.imported_sales;
		},
		export_as_JSON: function() {
			var json = _super_order.export_as_JSON.apply(this,arguments);
			json.imported_sales = this.imported_sales || [];
			return json;
		},

		init_from_JSON: function(json){
			_super_order.init_from_JSON.apply(this,arguments);
			this.imported_sales = json.imported_sales || [];
		},
	});

});