from django.shortcuts import render, redirect
from django.views.generic.edit import FormView
from django.views.generic import ListView
from django.utils.decorators import method_decorator
from fcuser.decorators import login_required
from django.db import transaction
from .forms import Registerform
from order.models import Order
from orderitem.models import OrderItem
from product.models import Product
from fcuser.models import Fcuser
from http import cookies
# Create your views here.

'''
@method_decorator(login_required, name='dispatch')
class OrderCreate(FormView):
  form_class = Registerform
  success_url = '/product/'


  def form_valid(self, form):
    # with transaction.atomic():
    #   prod = Product.objects.get(pk=form.data.get('product'))
    #   order = Order(
    #     quantity=form.data.get('quantity'),
    #     product = prod,
    #     fcuser = Fcuser.objects.get(email=self.request.session.get('user'))
    #   )
    #   order.save()
    #   prod.stock -= int(form.data.get('quantity'))
    #   prod.save()
    return super().form_valid(form)

  def form_invalid(self, form): # 수량이라던가 제품값이 없어서 실패하는 경우 돌아갈 페이지 지정하기 위해 사용
    return redirect('/product/' + str(form.data.get('product')))
  # class 기반의 view 안에 기본적으로 내장되있는 함수 > form을 생성할때 인자 전달할것들 정하기 위해 사용 > request 전달하기 위해 사용
  # def get_form_kwargs()
  # 기존에 자동으로 생성되던 인자값과 request 도 같이 보내겠다!
  def get_form_kwargs(self, **kwargs): 
    kw = super().get_form_kwargs(**kwargs)
    kw.update({
      'request' : self.request
    })
    return kw
'''

# @method_decorator(login_required, name='dispatch')
# class OrderList(ListView):
#   # model = Order # 자신이 주문한것만 보이게 하기위해 filter 적용(하단의 get_queryset > session 접근하기위해 사용하는 함수)
#   template_name = 'order.html'
#   context_object_name = 'order_list' # attribute name 설정 > 안할시 object_list

#   def get_queryset(self, **kwargs):
#     queryset = Order.objects.all()
#     print(queryset)
#     # queryset = Order.objects.filter(fcuser__email=self.request.session.get('user'))
#     return queryset

def OrderList(request):
  if request.method == 'GET':
    ordering = request.GET.get('ordering', 'ordernum')
    queryset = Order.objects.all().order_by(ordering)
    return render(request, 'order.html', {'order_list' : queryset, 'ordering' : ordering})

# @method_decorator(login_required, name='dispatch')
# class OrderDetail(ListView):
#   # model = Order # 자신이 주문한것만 보이게 하기위해 filter 적용(하단의 get_queryset > session 접근하기위해 사용하는 함수)
#   template_name = 'order_detail.html'
#   context_object_name = 'order_items' # attribute name 설정 > 안할시 object_list

#   def get_queryset(self, **kwargs):
#     r2 = Order.objects.get(ordernum=24)
#     queryset = r2.orderitem_set.all()
#     print(queryset)
#     return queryset

def OrderDetail(request, pk):
  if request.method == 'GET':
    r2 = Order.objects.get(ordernum=pk)
    queryset = r2.orderitem_set.all()
    print(queryset)
    return render(request, 'order_detail.html', {'order_items' : queryset})



def cart(request):
  if request.method == 'GET':
    if not request.session.get('user'):
      return redirect('/login')
    return render(request, 'cart.html')

def orderCreate(request):
  if request.method == 'POST':
    orderProductList = request.POST.get('orderProductList', None)
    if orderProductList:
      result = orderProductList.split('%&key%&')[:-1]
      check = True

      for v in result:
        prod = Product.objects.get(name=v)
        quantity = request.POST.get(v,0)
        if (prod.stock <= int(quantity)):
          check = False
      
      if check == True:
        order = Order(
          fcuser = Fcuser.objects.get(email=request.session.get('user'))
        )
        order.save()
        for v in result:
          prod = Product.objects.get(name=v)
          quantity = request.POST.get(v,0)
          
          orderitem = OrderItem(
            order = order,
            product = prod,
            quantity = quantity
          )
          orderitem.save()
          prod.stock -= int(quantity)
          prod.save()

    return redirect('/')

