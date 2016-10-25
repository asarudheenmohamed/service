var MagentoAPI = require('magento');
var magento = new MagentoAPI({
  host: 'tendercuts.in',
  port: 80,
  path: '/index.php/api/xmlrpc/',
  login: 'admin',
  pass: 'Tendercuts123!',
  secure: true
});


magento.salesOrder.list(
       {
            filters: { 
                'created_at': {'from': new Date("August 10, 2016 10:10:10"),
                              'to': new Date("August 11, 2016 10:10:10")},
                'status' : {
                    'in' : ['pending']
                }
            },
        }, function(err, result) {
                console.log(err)
                console.log('no of orders: ', result.length);
            }
        );

