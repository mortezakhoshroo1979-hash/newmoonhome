/* --------------------------------------------------
   اسکریپت‌های اصلی قالب NEWMOON HOME
   -------------------------------------------------- */

document.addEventListener('DOMContentLoaded', function () {
    if (typeof AOS !== 'undefined') {
        AOS.init({
            duration: 850,
            once: true,
            offset: 50
        });
    }

    // تغییر حالت نمایش گرید و لیست در صفحه محصولات
    const viewButtons = document.querySelectorAll('.view-btn');
    const productListGrid = document.getElementById('productListGrid');

    if (viewButtons.length && productListGrid) {
        viewButtons.forEach((button) => {
            button.addEventListener('click', function () {
                viewButtons.forEach(btn => btn.classList.remove('active'));
                this.classList.add('active');

                const view = this.dataset.view;
                if (view === 'list') {
                    productListGrid.classList.add('list-view');
                    productListGrid.querySelectorAll('.product-view-item').forEach((item) => {
                        item.className = 'col-12 product-view-item';
                    });
                } else {
                    productListGrid.classList.remove('list-view');
                    productListGrid.querySelectorAll('.product-view-item').forEach((item) => {
                        item.className = 'col-md-6 col-xl-4 product-view-item';
                    });
                }
            });
        });
    }

    // شبیه‌سازی ساده به‌روزرسانی سبد خرید
    document.querySelectorAll('.quantity-input').forEach((input) => {
        input.addEventListener('change', function () {
            if (parseInt(this.value, 10) < 1 || Number.isNaN(parseInt(this.value, 10))) {
                this.value = 1;
            }
        });
    });

    document.querySelectorAll('.remove-btn').forEach((button) => {
        button.addEventListener('click', function () {
            const row = this.closest('tr');
            if (row) {
                row.style.opacity = '0';
                setTimeout(() => row.remove(), 250);
            }
        });
    });
});

// پیشنهاد جستجو با Alpine.js
function searchSuggest() {
    return {
        query: '',
        open: false,
        items: [
            { name: 'مبل لوکس مدل آتریا', url: '/products/detail/' },
            { name: 'سرویس خواب الیت', url: '/products/detail/' },
            { name: 'میز ناهارخوری مون', url: '/products/detail/' },
            { name: 'کنسول مینیمال نوا', url: '/products/detail/' },
            { name: 'میز جلو مبلی هارمونیا', url: '/products/detail/' }
        ],
        filtered: [],
        updateSuggestions() {
            const q = this.query.trim();
            if (!q.length) {
                this.filtered = [];
                return;
            }
            this.filtered = this.items.filter(item => item.name.includes(q)).slice(0, 5);
        }
    }
}

// گالری صفحه محصول
function gallerySwitcher() {
    const defaultImages = [
        'https://images.unsplash.com/photo-1505693416388-ac5ce068fe85?q=80&w=1000&auto=format&fit=crop',
        'https://images.unsplash.com/photo-1555041469-a586c61ea9bc?q=80&w=1000&auto=format&fit=crop',
        'https://images.unsplash.com/photo-1493663284031-b7e3aefcae8e?q=80&w=1000&auto=format&fit=crop',
        'https://images.unsplash.com/photo-1519947486511-46149fa0a254?q=80&w=1000&auto=format&fit=crop'
    ];

    return {
        images: defaultImages,
        activeImage: defaultImages[0]
    }
}

// محاسبه لحظه‌ای قیمت در صفحه محصول
function productCustomizer() {
    return {
        basePrice: 48000000,
        size: 0,
        color: 0,
        fabric: 0,
        qty: 1,
        totalPrice: 48000000,
        recalculate() {
            this.totalPrice = this.basePrice + Number(this.size) + Number(this.color) + Number(this.fabric);
        },
        formattedPrice() {
            return new Intl.NumberFormat('fa-IR').format(this.totalPrice) + ' ریال';
        },
        increaseQty() {
            this.qty++;
        },
        decreaseQty() {
            if (this.qty > 1) {
                this.qty--;
            }
        }
    }
}
