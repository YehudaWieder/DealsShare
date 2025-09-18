import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import random
from werkzeug.datastructures import FileStorage


from routes.auth_routes import insert_new_user
from routes.product_routes import insert_new_product
from config import DB_PATH

DB_PATH = DB_PATH


def seed_data():
    users = [
    {"email": "admin@deals.com", "first_name": "David", "last_name": "Levy", "gender": "male", "password": "123456", "role": "admin"},
    {"email": "maria.smith@example.com", "first_name": "Maria", "last_name": "Smith", "gender": "female", "password": "123456", "role": "user"},
    {"email": "john.doe@example.com", "first_name": "John", "last_name": "Doe", "gender": "male", "password": "123456", "role": "user"},
    {"email": "emma.jones@example.com", "first_name": "Emma", "last_name": "Jones", "gender": "female", "password": "123456", "role": "user"},
    {"email": "liam.brown@example.com", "first_name": "Liam", "last_name": "Brown", "gender": "male", "password": "123456", "role": "user"},
    {"email": "olivia.davis@example.com", "first_name": "Olivia", "last_name": "Davis", "gender": "female", "password": "123456", "role": "user"},
    {"email": "noah.wilson@example.com", "first_name": "Noah", "last_name": "Wilson", "gender": "male", "password": "123456", "role": "user"},
    {"email": "sophia.martin@example.com", "first_name": "Sophia", "last_name": "Martin", "gender": "female", "password": "123456", "role": "user"},
    {"email": "james.moore@example.com", "first_name": "James", "last_name": "Moore", "gender": "male", "password": "123456", "role": "user"},
    {"email": "mia.taylor@example.com", "first_name": "Mia", "last_name": "Taylor", "gender": "female", "password": "123456", "role": "user"}
]
        # Sample products
    products = [
    {"seller_email": "maria.smith@example.com", "name": "Coffee Table", "features": "wood,modern,compact", "free_shipping": 1, "description": "Stylish oak coffee table, perfect for any living room.", "category": "home", "regular_price": 120.0, "discount_price": 99.99, "image_path": "/home/mefathim/Downloads/img/coffee_table.png", "link": "https://example.com/coffee_table"},
    {"seller_email": "john.doe@example.com", "name": "Sofa", "features": "leather,comfortable,spacious", "free_shipping": 1, "description": "Luxurious leather sofa that seats three people comfortably.", "category": "home", "regular_price": 850.0, "discount_price": 699.99, "image_path": "/home/mefathim/Downloads/img/sofa.png", "link": "https://example.com/sofa"},
    {"seller_email": "emma.jones@example.com", "name": "Clock", "features": "modern,wall,quartz", "free_shipping": 0, "description": "Elegant wall clock with silent quartz movement.", "category": "home", "regular_price": 45.0, "discount_price": 39.99, "image_path": "/home/mefathim/Downloads/img/clock.jpeg", "link": "https://example.com/clock"},
    {"seller_email": "liam.brown@example.com", "name": "Vase", "features": "ceramic,decorative,handmade", "free_shipping": 1, "description": "Beautiful handmade ceramic vase for flowers.", "category": "home", "regular_price": 60.0, "discount_price": 49.99, "image_path": "/home/mefathim/Downloads/img/vase.png", "link": "https://example.com/vase"},
    {"seller_email": "olivia.davis@example.com", "name": "Bedside Lamp", "features": "led,adjustable,modern", "free_shipping": 1, "description": "LED bedside lamp with adjustable brightness.", "category": "home", "regular_price": 35.0, "discount_price": 29.99, "image_path": "/home/mefathim/Downloads/img/bedside_lamp.jpeg", "link": "https://example.com/bedside_lamp"},
    {"seller_email": "noah.wilson@example.com", "name": "Wireless Headphones", "features": "bluetooth,noise-canceling,over-ear", "free_shipping": 0, "description": "High-quality wireless headphones with noise-canceling.", "category": "electronics", "regular_price": 150.0, "discount_price": 129.99, "image_path": "/home/mefathim/Downloads/img/wireless_headphones.png", "link": "https://example.com/wireless_headphones"},
    {"seller_email": "sophia.martin@example.com", "name": "Bluetooth Speaker", "features": "portable,waterproof,wireless", "free_shipping": 1, "description": "Portable Bluetooth speaker with waterproof design.", "category": "electronics", "regular_price": 80.0, "discount_price": 69.99, "image_path": "/home/mefathim/Downloads/img/bluetooth_speaker.png", "link": "https://example.com/bluetooth_speaker"},
    {"seller_email": "james.moore@example.com", "name": "Smart Watch", "features": "fitness,waterproof,notifications", "free_shipping": 0, "description": "Smart watch with fitness tracking and notifications.", "category": "electronics", "regular_price": 200.0, "discount_price": 179.99, "image_path": "/home/mefathim/Downloads/img/smart_watch.png", "link": "https://example.com/smart_watch"},
    {"seller_email": "mia.taylor@example.com", "name": "Power Bank", "features": "portable,high-capacity,fast-charge", "free_shipping": 1, "description": "High-capacity portable power bank with fast charging.", "category": "electronics", "regular_price": 50.0, "discount_price": 39.99, "image_path": "/home/mefathim/Downloads/img/power_bank.jpeg", "link": "https://example.com/power_bank"},
    {"seller_email": "maria.smith@example.com", "name": "T-Shirt", "features": "cotton,casual,comfortable", "free_shipping": 1, "description": "Soft cotton T-shirt available in multiple colors.", "category": "clothing", "regular_price": 25.0, "discount_price": 19.99, "image_path": "/home/mefathim/Downloads/img/t-shirt.jpeg", "link": "https://example.com/tshirt"},
    {"seller_email": "john.doe@example.com", "name": "Jeans", "features": "denim,classic,slim-fit", "free_shipping": 1, "description": "Classic slim-fit denim jeans for everyday wear.", "category": "clothing", "regular_price": 60.0, "discount_price": 49.99, "image_path": "/home/mefathim/Downloads/img/jeans.png", "link": "https://example.com/jeans"},
    {"seller_email": "emma.jones@example.com", "name": "Sweater", "features": "wool,warm,soft", "free_shipping": 0, "description": "Warm and soft wool sweater for winter.", "category": "clothing", "regular_price": 70.0, "discount_price": 59.99, "image_path": "/home/mefathim/Downloads/img/sweater.png", "link": "https://example.com/sweater"},
    {"seller_email": "liam.brown@example.com", "name": "Jacket", "features": "waterproof,windproof,lightweight", "free_shipping": 1, "description": "Waterproof and lightweight jacket for all seasons.", "category": "clothing", "regular_price": 120.0, "discount_price": 99.99, "image_path": "/home/mefathim/Downloads/img/jacket.png", "link": "https://example.com/jacket"},
    {"seller_email": "olivia.davis@example.com", "name": "Sneakers", "features": "comfortable,breathable,running", "free_shipping": 1, "description": "Comfortable sneakers suitable for running and casual wear.", "category": "shoes", "regular_price": 90.0, "discount_price": 79.99, "image_path": "/home/mefathim/Downloads/img/sneakers.png", "link": "https://example.com/sneakers"},
    {"seller_email": "noah.wilson@example.com", "name": "Brown Leather Shoes", "features": "leather,elegant,formal", "free_shipping": 0, "description": "Elegant brown leather shoes for formal occasions.", "category": "shoes", "regular_price": 130.0, "discount_price": 109.99, "image_path": "/home/mefathim/Downloads/img/browen_lether_shoes.png", "link": "https://example.com/brown_leather_shoes"},
    {"seller_email": "sophia.martin@example.com", "name": "Women Sandals", "features": "comfortable,summer,elegant", "free_shipping": 1, "description": "Elegant summer sandals for women.", "category": "shoes", "regular_price": 55.0, "discount_price": 45.99, "image_path": "/home/mefathim/Downloads/img/women_sandals.png", "link": "https://example.com/women_sandals"},
    {"seller_email": "james.moore@example.com", "name": "Boots", "features": "leather,warm,durable", "free_shipping": 0, "description": "Durable leather boots for cold weather.", "category": "shoes", "regular_price": 150.0, "discount_price": 129.99, "image_path": "/home/mefathim/Downloads/img/boots.png", "link": "https://example.com/boots"},
    {"seller_email": "mia.taylor@example.com", "name": "Flip Flops", "features": "casual,lightweight,summer", "free_shipping": 1, "description": "Lightweight flip flops for casual summer use.", "category": "shoes", "regular_price": 20.0, "discount_price": 14.99, "image_path": "/home/mefathim/Downloads/img/flip_flops.png", "link": "https://example.com/flip_flops"},
    {"seller_email": "maria.smith@example.com", "name": "Teddy Bear", "features": "soft,cute,plush", "free_shipping": 1, "description": "Cute plush teddy bear for children.", "category": "toys", "regular_price": 30.0, "discount_price": 24.99, "image_path": "/home/mefathim/Downloads/img/teddy_bear.png", "link": "https://example.com/teddy_bear"},
    {"seller_email": "john.doe@example.com", "name": "Building Blocks", "features": "colorful,educational,safe", "free_shipping": 1, "description": "Colorful building blocks set for creative play.", "category": "toys", "regular_price": 40.0, "discount_price": 34.99, "image_path": "/home/mefathim/Downloads/img/building_blocks.png", "link": "https://example.com/building_blocks"},
    {"seller_email": "emma.jones@example.com", "name": "Remote Control Car", "features": "fast,fun,durable", "free_shipping": 0, "description": "Fast remote control car for kids and teens.", "category": "toys", "regular_price": 60.0, "discount_price": 49.99, "image_path": "/home/mefathim/Downloads/img/romote_control_car.png", "link": "https://example.com/remote_control_car"},
    {"seller_email": "liam.brown@example.com", "name": "Puzzle", "features": "educational,fun,colorful", "free_shipping": 1, "description": "Challenging and fun puzzle for all ages.", "category": "toys", "regular_price": 25.0, "discount_price": 19.99, "image_path": "/home/mefathim/Downloads/img/puzzle.png", "link": "https://example.com/puzzle"},
    {"seller_email": "olivia.davis@example.com", "name": "Action Figure", "features": "collectible,detailed,plastic", "free_shipping": 1, "description": "High-quality action figure for collectors and kids.", "category": "toys", "regular_price": 35.0, "discount_price": 29.99, "image_path": "/home/mefathim/Downloads/img/Action_figure.png", "link": "https://example.com/action_figure"},
    {"seller_email": "noah.wilson@example.com", "name": "Plate Set", "features": "ceramic,dinnerware,modern", "free_shipping": 0, "description": "Elegant ceramic plate set for everyday meals.", "category": "kitchen", "regular_price": 45.0, "discount_price": 39.99, "image_path": "/home/mefathim/Downloads/img/plate_set.png", "link": "https://example.com/plate_set"},
    {"seller_email": "sophia.martin@example.com", "name": "Knife Set", "features": "stainless,sharp,ergonomic", "free_shipping": 1, "description": "Stainless steel knife set for the modern kitchen.", "category": "kitchen", "regular_price": 80.0, "discount_price": 69.99, "image_path": "/home/mefathim/Downloads/img/knife_set.jpeg", "link": "https://example.com/knife_set"},
    {"seller_email": "james.moore@example.com", "name": "Coffee Maker", "features": "automatic,modern,compact", "free_shipping": 1, "description": "Automatic coffee maker with compact design.", "category": "kitchen", "regular_price": 120.0, "discount_price": 99.99, "image_path": "/home/mefathim/Downloads/img/coffee_maker.jpeg", "link": "https://example.com/coffee_maker"},
    {"seller_email": "mia.taylor@example.com", "name": "Blender Machine", "features": "powerful,multi-speed,compact", "free_shipping": 0, "description": "Multi-speed blender perfect for smoothies and sauces.", "category": "kitchen", "regular_price": 75.0, "discount_price": 59.99, "image_path": "/home/mefathim/Downloads/img/Blender_machine.png", "link": "https://example.com/blender_machine"},
    {"seller_email": "maria.smith@example.com", "name": "Stainless Steel Pan", "features": "durable,non-stick,heat-resistant", "free_shipping": 1, "description": "Durable stainless steel pan for everyday cooking.", "category": "kitchen", "regular_price": 55.0, "discount_price": 44.99, "image_path": "/home/mefathim/Downloads/img/stainless_steel_pan.png", "link": "https://example.com/stainless_steel_pan"},
    {"seller_email": "john.doe@example.com", "name": "Gold Necklace", "features": "elegant,shiny,classic", "free_shipping": 1, "description": "Elegant gold necklace to complement any outfit.", "category": "jewellery", "regular_price": 200.0, "discount_price": 179.99, "image_path": "/home/mefathim/Downloads/img/gold_necklace.png", "link": "https://example.com/gold_necklace"},
    {"seller_email": "emma.jones@example.com", "name": "Silver Ring", "features": "sterling,shiny,classic", "free_shipping": 0, "description": "Sterling silver ring, elegant and durable.", "category": "jewellery", "regular_price": 80.0, "discount_price": 69.99, "image_path": "/home/mefathim/Downloads/img/silver_ring.png", "link": "https://example.com/silver_ring"},
    {"seller_email": "liam.brown@example.com", "name": "Pearl Earrings", "features": "elegant,classic,lightweight", "free_shipping": 1, "description": "Classic pearl earrings for a sophisticated look.", "category": "jewellery", "regular_price": 120.0, "discount_price": 99.99, "image_path": "/home/mefathim/Downloads/img/pearl_earrings.png", "link": "https://example.com/pearl_earrings"},
    {"seller_email": "olivia.davis@example.com", "name": "Diamond Bracelet", "features": "luxury,shiny,delicate", "free_shipping": 1, "description": "Delicate diamond bracelet for special occasions.", "category": "jewellery", "regular_price": 500.0, "discount_price": 449.99, "image_path": "/home/mefathim/Downloads/img/diamond_bracelet.png", "link": "https://example.com/diamond_bracelet"},
    {"seller_email": "noah.wilson@example.com", "name": "Gemstone Pendant", "features": "colorful,elegant,classic", "free_shipping": 0, "description": "Beautiful gemstone pendant for necklaces.", "category": "jewellery", "regular_price": 150.0, "discount_price": 129.99, "image_path": "/home/mefathim/Downloads/img/gemstone_pendant.png", "link": "https://example.com/gemstone_pendant"},
    {"seller_email": "sophia.martin@example.com", "name": "Office Chair", "features": "ergonomic,comfortable,adjustable", "free_shipping": 1, "description": "Ergonomic office chair with adjustable height.", "category": "office", "regular_price": 200.0, "discount_price": 179.99, "image_path": "/home/mefathim/Downloads/img/office_chair.png", "link": "https://example.com/office_chair"},
    {"seller_email": "james.moore@example.com", "name": "Wooden Office Desk", "features": "spacious,sturdy,classic", "free_shipping": 1, "description": "Spacious wooden office desk for work and study.", "category": "office", "regular_price": 350.0, "discount_price": 299.99, "image_path": "/home/mefathim/Downloads/img/wooden_office_desk.png", "link": "https://example.com/wooden_office_desk"},
    {"seller_email": "mia.taylor@example.com", "name": "Desk Lamp", "features": "led,adjustable,modern", "free_shipping": 0, "description": "Adjustable LED desk lamp for office or study.", "category": "office", "regular_price": 45.0, "discount_price": 39.99, "image_path": "/home/mefathim/Downloads/img/desk_lamp.png", "link": "https://example.com/desk_lamp"},
    {"seller_email": "maria.smith@example.com", "name": "Stationery Organizer", "features": "compact,practical,modern", "free_shipping": 1, "description": "Keep your desk neat with this stationery organizer.", "category": "office", "regular_price": 25.0, "discount_price": 19.99, "image_path": "/home/mefathim/Downloads/img/stationery_organizer.png", "link": "https://example.com/stationery_organizer"},
    {"seller_email": "john.doe@example.com", "name": "Laptop Stand", "features": "portable,ergonomic,aluminum", "free_shipping": 1, "description": "Portable ergonomic laptop stand made of aluminum.", "category": "office", "regular_price": 50.0, "discount_price": 44.99, "image_path": "/home/mefathim/Downloads/img/laptop_stand.png", "link": "https://example.com/laptop_stand"}
]

    
    for user in users:
        form_data = {
            "first_name": user["first_name"],
            "last_name": user["last_name"],
            "email": user["email"],
            "password": user["password"],
            "role": user["role"]
        }

        result = insert_new_user(form_data)
        if result.get("success"):
            print(f"User {user['email']} inserted successfully")
        else:
            print(f"Error inserting user {user['email']}: {result.get('message')}")


    random.shuffle(products)

    for p in products:
        seller_email = p["seller_email"]
        form_data = {
            "name": p["name"],
            "features": p["features"],
            "free_shipping": p["free_shipping"],
            "description": p["description"],
            "category": p["category"],
            "regular_price": p["regular_price"],
            "discount_price": p["discount_price"],
            "link": p["link"]
        }

        file = None
        if os.path.exists(p["image_path"]):
            file = FileStorage(open(p["image_path"], "rb"), filename=os.path.basename(p["image_path"]))

        result = insert_new_product(form_data, file, seller_email)
        if result.get("success"):
            print(f"Product {p['name']} inserted successfully")
        else:
            print(f"Error inserting product {p['name']}: {result.get('message')}")

if __name__ == "__main__":
    seed_data()
    print("Seed data inserted successfully!")
