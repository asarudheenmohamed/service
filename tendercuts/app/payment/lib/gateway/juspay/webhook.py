"""Triggered after sometime, mostly from webhooks or polling.

We get two event callbacks
1. ORDER_SUCCEEDED - handled by JuspayOrderSucceededProcessor
2. ORDER_REFUNDED - currently ignored

for now we are only interested in ORDER_SUCCEEDED

"""
"""
# if payload.get('event_name', None) != 'ORDER_SUCCEEDED':
#     raise ValueError("Invalid payload {}".format(payload))

processes the payload provided by juspay and updates the order status
{u'event_name': u'ORDER_SUCCEEDED', 
    u'date_created': u'2018-05-08T06:29:14Z', 
    u'content': {
        u'order': {u'auth_type': u'THREE_DS', 
            u'txn_id': u'tendercuts-700033259-1',
            u'payment_method': u'VISA', 
    u'payment_links': {u'mobile': u'https://sandbox.juspay.in/merchant/pay/ord_36b2e1b7ee7c4598b8f02e14049b6ff8?mobile=true', u'web': u'https://sandbox.juspay.in/merchant/pay/ord_36b2e1b7ee7c4598b8f02e14049b6ff8', u'iframe': u'https://sandbox.juspay.in/merchant/ipay/ord_36b2e1b7ee7c4598b8f02e14049b6ff8'}, 
    u'bank_error_code': u'', u'currency': u'INR', u'customer_email': u'5799766456@email.com', 
    u'id': u'ord_36b2e1b7ee7c4598b8f02e14049b6ff8', u'gateway_id': 23, u'amount': 154, 
    u'payment_gateway_response': {u'rrn': u'', u'auth_id_code': u'NA', u'txn_id': u'tendercuts-700033259-1', u'epg_txn_id': u'pay_A8UwNYDlM7Ix9m', u'created': u'2018-05-08T06:29:14Z', u'resp_code': u'captured', u'resp_message': u'captured'}, 
    u'customer_id': u'juspay_50001', u'status': u'CHARGED', 
    u'amount_refunded': 0, u'txn_uuid': u'1mrnsctswpre8yti', 
    u'status_id': 21, 
    u'order_id': u'700033259', u'refunded': False, u'customer_phone': u'9710243651', u'udf8': u'', u'merchant_id': u'tendercuts', u'card': {u'name_on_card': u'', u'last_four_digits': u'', u'card_reference': u'0fc80a15caea1c33c74bcccece6f1f3c', u'card_fingerprint': u'78g5l1fp62obpivbqsved6dsgb', u'using_saved_card': True, u'card_type': u'DEBIT', u'card_issuer': u'', u'expiry_year': u'2018', u'card_brand': u'VISA', u'saved_to_locker': True, u'expiry_month': u'08', u'card_isin': u'424242'}, u'product_id': u'', u'payment_method_type': u'CARD', u'udf10': u'', u'bank_error_message': u'', u'udf1': u'', u'udf3': u'', u'udf2': u'', u'udf5': u'', u'udf4': u'', u'udf7': u'', u'udf6': u'', u'udf9': u'', u'date_created': u'2018-05-08T06:29:08Z', u'return_url': u'http://staging.tendercuts.in:82/payment/juspay'}}, u'id': u'evt_1vol8hxlgpmx53ee'}

"""
from app.core import models as core_models
from app.core.lib import order_controller as controller
from .mixin import JuspayMixin
from app.driver import tasks

class JuspayOrderSuccessProcessor(JuspayMixin):

    @classmethod
    def from_payload(cls, payload):
        """Generates a processor instance from the payload.

        params:
            payload: dict containing event name and details

        raises:
            ValueError: In case of invalid payload

        """
        event_name = payload['event_name']
        # extract order id
        content = payload.get('content', {})
        order = content.get('order', {})
        order_id = order.get('order_id', None)

        if not order_id:
            raise ValueError("Invalid order id {}".format(payload))

        order = core_models.SalesFlatOrder.objects.filter(
            increment_id=order_id).first()

        if not order:
            raise ValueError("Order not found {}".format(order_id))

        return cls(order)


    def __init__(self, order):
        self.order = order

    def action_order_confirm(self):
        """Confirms the orders and sends an sms.

        This will be triggered only in cases of pending, processing,
        out_delivery & complete.

        in case of payment_pending status, confirm the order.
        """

        if self.order.status == "pending_payment":
            # update status to pending
            ord_ctrl = controller.OrderController(None, self.order)
            ord_ctrl.payment_success()

        # in cases of any other status, it means that we have
        # started processing the order, so just update the payment
        # method.
        payment = self.order.payment.all()[0]
        payment.method = "juspay"
        payment.save()

        # SMS TRIGGERING
        tasks.send_sms.delay(self.order.increment_id, 'payment_confirmation')


    def action_order_refund(self):
        self.juspay.Orders.refund(
            unique_request_id=self.order.increment_id,
            order_id=self.order.increment_id)

        # SMS TRIGGERING
        tasks.send_sms.delay(self.order.increment_id, 'payment_refunded')

    def execute(self):
        # XXX
        actions = {
            'pending_payment': self.action_order_confirm,
            'pending': self.action_order_confirm,  # COD converts
            'scheduled_order': self.action_order_confirm,  # COD converts
            'processing': self.action_order_confirm,
            'out_delivery': self.action_order_confirm,

            'canceled': self.action_order_refund,
            'closed': self.action_order_refund
        }

        status = self.order.status
        payment = self.order.payment.all()[0]

        # duplicate callback
        if status in ("pending", "scheduled_order") and payment.method == "juspay":
            return

        action = actions.get(status, None)

        if action:
            action()
