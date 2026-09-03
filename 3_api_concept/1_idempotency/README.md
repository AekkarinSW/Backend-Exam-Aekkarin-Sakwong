## Question
![](/assets/q_idempotency.png)

## Response Section

Idempotency ใน RESTful API หมายถึง การส่ง request เดิมซ้ำหลายครั้งแล้วผลกระทบสุดท้ายต่อระบบยังเหมือนกับการส่งครั้งเดียว

ตัวอย่างที่พบบ่อยคือ client ส่งคำสั่งสร้าง order แล้วเกิด network timeout แม้ฝั่ง server จะสร้าง order สำเร็จไปแล้ว หาก client retry โดยไม่มีการป้องกัน ระบบอาจสร้าง order ซ้ำ

โดยทั่วไป

- `GET` ควรอ่านข้อมูลอย่างเดียว จึงเป็น idempotent
- `PUT` ส่งข้อมูลเดิมซ้ำแล้ว resource ควรอยู่ในสถานะเดิม
- `DELETE` เป็น idempotent ในแง่ผลลัพธ์สุดท้าย เพราะลบซ้ำแล้ว resource ก็ยังไม่มีอยู่
- `POST` มักไม่เป็น idempotent เพราะแต่ละครั้งอาจสร้าง resource ใหม่

HTTP status หรือ response ของแต่ละครั้งไม่จำเป็นต้องเหมือนกัน สิ่งสำคัญคือผลกระทบสุดท้ายต่อข้อมูลต้องไม่ถูกทำซ้ำ

### ตัวอย่างด้วย Python และ Django REST Framework

```python
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response


created_orders = {}


@api_view(["POST"])
def create_order(request):
    idempotency_key = request.headers.get("Idempotency-Key")

    if not idempotency_key:
        return Response(
            {"detail": "Idempotency-Key is required"},
            status=status.HTTP_400_BAD_REQUEST,
        )

    if idempotency_key in created_orders:
        return Response(
            created_orders[idempotency_key],
            status=status.HTTP_201_CREATED,
        )

    order = {
        "id": len(created_orders) + 1,
        "product_id": request.data.get("product_id"),
        "quantity": request.data.get("quantity"),
    }
    created_orders[idempotency_key] = order

    return Response(order, status=status.HTTP_201_CREATED)
```

เมื่อ client ส่ง `Idempotency-Key` เดิม ระบบจะคืน order เดิมแทนการสร้างรายการใหม่

ตัวอย่างนี้ใช้ `dict` เพื่อให้เห็นแนวคิดได้ง่ายเท่านั้น ในระบบจริงควรเก็บ key และผลลัพธ์ไว้ใน database หรือ Redis พร้อม unique constraint หรือ atomic operation เพื่อกัน race condition นอกจากนี้ควรกำหนดอายุของ key และตรวจว่า key เดิมไม่ได้ถูกนำไปใช้กับ request body คนละชุด
