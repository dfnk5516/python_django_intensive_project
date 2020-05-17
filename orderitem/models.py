from django.db import models
from order.models import Order

# Create your models here.
class OrderItem(models.Model):
  order = models.ForeignKey(Order, on_delete=models.CASCADE, verbose_name='주문 번호')
  # ordernum = models.ForeignKey('order.Order', on_delete=models.CASCADE, verbose_name='주문 번호')
  product = models.ForeignKey('product.Product', on_delete=models.CASCADE, verbose_name='상품')
  quantity = models.IntegerField(verbose_name='수량')
  
  # fcuser = models.ForeignKey('fcuser.Fcuser', on_delete=models.CASCADE, verbose_name='사용자')
  # register_date = models.DateTimeField(auto_now_add=True, verbose_name='등록날짜')

  def __str__(self):
    return str(self.product)

  class Meta:
    db_table = 'fastcampus_orderItem'
    verbose_name = '주문제품'
    verbose_name_plural = '주문제품'