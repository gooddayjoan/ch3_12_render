import os
import django
import random

# 設定 Django 環境
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'ch3_12_render.settings')  # 改成你的 settings 模組路徑
django.setup()

from myapp.models import Member, ProductType, Product, Price, Color, Size, ProductImage, ProductColorSize

# 清空舊資料（可選）
Member.objects.all().delete()
ProductType.objects.all().delete()
Product.objects.all().delete()
Price.objects.all().delete()
Color.objects.all().delete()
Size.objects.all().delete()
ProductImage.objects.all().delete()
ProductColorSize.objects.all().delete()

# 建立會員
member_names = ['王小明', '林美麗', '陳大文', '張怡君', '李志強', '吳惠芳']
for name in member_names:
    Member.objects.create(
        name=name,
        email=f"{name}@example.com".replace(" ", "").lower(),
        address=f"{name} 的地址"
    )

# 建立商品類型
type_names = ['Computer', 'Peripheral', 'Display']
product_types = [ProductType.objects.create(type_name=name) for name in type_names]

# 建立顏色
color_names = ['黑色', '銀色', '白色', '灰色']
colors = [Color.objects.create(color_name=c) for c in color_names]

# 建立尺寸
size_names = ['小型', '中型', '大型']
sizes = [Size.objects.create(size_name=s) for s in size_names]

# 電子商品名稱清單
electronic_product_names = [
    '電腦主機',
    '顯示器',
    '鍵盤',
    '滑鼠',
    '筆記型電腦',
    '印表機',
    '掃描器',
    '喇叭',
    '外接硬碟',
    '無線路由器'
]

# 建立商品與相關資料
for i, name in enumerate(electronic_product_names):
    ptype = random.choice(product_types)
    product = Product.objects.create(
        name=name,
        description=f"{name} 的詳細描述",
        quantity=0,  # 初始為 0，稍後再更新
        type=ptype
    )

    # 加入價格
    Price.objects.create(
        product=product,
        price=round(random.uniform(1000, 50000), 2)
    )

    # 加入圖片
    ProductImage.objects.create(
        product=product,
        image_url=f"https://example.com/electronic_{i+1}.jpg"
    )

    # 加入顏色與尺寸對應
    selected_colors = random.sample(colors, 2)
    selected_sizes = random.sample(sizes, 2)
    total_quantity = 0
    for color in selected_colors:
        for size in selected_sizes:
            qty = random.randint(1, 20)
            ProductColorSize.objects.create(
                product=product,
                color=color,
                size=size,
                available_quantity=qty
            )
            total_quantity += qty

    # 更新商品總庫存數量
    product.quantity = total_quantity
    product.save()

print("✅ 資料建立完成！")
