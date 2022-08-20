odoo.define('pos_document_type_bds.model_doctype', function(require) {
"use strict";

var models = require('point_of_sale.models');
var _super_posmodel = models.PosModel.prototype;

models.PosModel = models.PosModel.extend({
	push_and_invoice_order: function(order) {
		var self = this;
		var rec = self.got_doctype_id(order);
		var order_id = self.db.add_order(order.export_as_JSON());
		var orders = self.db.get_order(order_id);
		orders['doctype_id'] = order['doctype_id'];
		self.flush_mutex.exec(function () {
			var done =  new Promise(function (resolveDone, rejectDone) {
				var transfer = self._flush_orders([orders], {timeout:30000, to_invoice:true});
			});
		});
		return _super_posmodel.push_and_invoice_order.apply(this, arguments);
	},
	push_single_order: function (order, opts) {
        opts = opts || {};
        const self = this;
        const order_id = self.db.add_order(order.export_as_JSON());
        var rec = self.got_doctype_id(order);

        return new Promise(function (resolve, reject) {
            self.flush_mutex.exec(function () {
                var order = self.db.get_order(order_id);
                order['doctype_id'] = rec
                if (order){
                    var flushed = self._flush_orders([order], opts);
                } else {
                    var flushed = Promise.resolve([]);
                }
                flushed.then(resolve, reject);

                return flushed;
            });
        });
    },

	got_doctype_id: function(order) {
		var id = order['doctype_id'];
		return id;
	},

	_flush_orders: function(orders, options) {
		var self = this;
		return _super_posmodel._flush_orders.apply(this, arguments);
	},

	_save_to_server: function (orders, options) {
		var self=this;
		return _super_posmodel._save_to_server.call(this, orders, options);
	}
});

});