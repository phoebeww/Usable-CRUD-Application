from flask import Flask, Markup
from flask import render_template
from flask import Response, request, jsonify
from flask import redirect, url_for
from urllib.parse import urlparse
import re
app = Flask(__name__)

data = [
    {
        "id": 1,
        "name": "Wanpo Tea Shop",
        "image": "https://s3-media0.fl.yelpcdn.com/bphoto/nGx1QxvVklgMWmq9rRLjcg/o.jpg",
        "description": """Wanpo Tea Shop in New York is a cozy spot for tea lovers, 
        known for its delicious Taiwanese boba teas. They offer a variety of flavors, 
        from classic milk tea to fruit teas and lattes, all made with fresh ingredients. 
        It's a great place to enjoy a tasty tea drink and relax in a friendly atmosphere. 
        Whether you're new to boba or a seasoned fan, Wanpo Tea Shop has something 
        special for everyone.""",
        "rating": "4.3",
        "address": "37 E 8th St, New York, NY 10003",
        "example_drinks": ["Matcha Red Bean Jelly Latte", "Purple Rice Taro Milk", 
                           "Passion Fruit Green Tea", "Brown Sugar Bubble With Milk"],
        "category": "Boba"
    },
    {
        "id": 2,
        "name": "Xing Fu Tang",
        "image": "https://s3-media0.fl.yelpcdn.com/bphoto/cyFHFEwKCRW738Fa2yW2Pg/o.jpg",
        "description": """Xing Fu Tang is celebrated for offering the finest hand-crafted 
        brown sugar boba from Taiwan, now available in the United States. They feature 
        an open kitchen concept, allowing customers to watch as boba pearls are freshly 
        made hourly and cooked to order, ensuring transparency and quality in every cup.""",
        "rating": "4.3",
        "address": "133 2nd Ave New York, NY 10003",
        "example_drinks": ["Gold Foil Boba Milk", "Herbal Jelly Boba Milk", 
                           "Boba Milk Tea Soft Serve", "Kirin Roasted Oolong Tea"],
        "category": "Boba"
    },
    {
        "id": 3,
        "name": "Harney & Sons SoHo",
        "image": "https://s3-media0.fl.yelpcdn.com/bphoto/rZah4y8IBd57nwmN6xvgRQ/o.jpg",
        "description": """Harney & Sons Fine Teas, founded in 1983 by John Harney, is 
        dedicated to delivering high-quality teas at reasonable prices. The company, 
        now led by Michael and Paul Harney, emphasizes tradition and innovation in their 
        tea selection, sourcing the finest teas worldwide. They aim to make tea shopping 
        and exploration a delightful experience, offering free domestic shipping with a 
        quality guarantee to ensure customer satisfaction.""",
        "rating": "4.3",
        "address": "433 Broome St Ground Fl New York, NY 10013",
        "example_drinks": ["Herbal Tea", "Black Tea Blend", "Iced Chai", "Blood Orange Tea"],
        "category": "Tea"
    },
    {
        "id": 4,
        "name": "Black Brick",
        "image": "https://s3-media0.fl.yelpcdn.com/bphoto/ZMALRM-BbdnPdqK_b05hzQ/o.jpg",
        "description": """Black Brick Coffee, located in Brooklyn, NY, offers a cozy spot 
        for coffee enthusiasts and pastry lovers. With its welcoming atmosphere, Black Brick 
        Coffee serves a variety of high-quality coffees, teas, and pastries. Their operating 
        hours cater to both early birds and evening dwellers, making it a versatile destination 
        for anyone looking to enjoy a great cup of coffee in a comfortable setting. """,
        "rating": "4.0",
        "address": "300 Bedford Ave Brooklyn, NY 11211",
        "example_drinks": ["Cold Brew", "Iced Coconut Matcha Latte", "Flat White", 
                           "Coconut Lavender Latte"],
        "category": "Coffee"
    },
    {
        "id": 5,
        "name": "Qahwah House",
        "image": "https://s3-media0.fl.yelpcdn.com/bphoto/xtIyvJ2azgI029NERntj0g/o.jpg",
        "description": """Qahwah House is a family-run business established in 2017, 
        specializing in premium Yemeni coffee without any added preservatives, artificial 
        additives, or flavors. Originating from Yemen, the birthplace of coffee, Qahwah 
        House offers an authentic experience with traditional Yemenite coffee, reflecting 
        a deep heritage and passion for coffee cultivated over generations.""",
        "rating": "4.7",
        "address": "162 Bedford Ave Brooklyn, NY 11249",
        "example_drinks": ["Adeni Chai", "Yameni Latte", "Jubani Coffee", "Mofawar Coffee"],
        "category": "Coffee"
    },
    {
        "id": 6,
        "name": "HEYTEA",
        "image": "https://s3-media0.fl.yelpcdn.com/bphoto/VI14EG6eAEKC6qi9BjlEBg/o.jpg",
        "description": """HeyTea, the renowned creator of cheese tea, made its debut in New 
        York City's Midtown in December. Originating from a modest beginning in Jiangbianli, 
        China, HeyTea has played a pivotal role in heralding the "New-Style Tea" era since 
        2012. The brand has since expanded its presence to over 600 stores across 40 cities, 
        including London, showcasing its commitment to using real tea leaves. HeyTea offers 
        a diverse range of beverages, from the original Very Grape Cheezo to Very Nectar Plum 
        and Roasted Brown Boba Milk, catering to adventurous drinkers and tea enthusiasts. """,
        "rating": "4.3",
        "address": "1407 Broadway New York, NY 10018",
        "example_drinks": ["Mango Grapefruit Sago", "Very Grape Cheese", 
                           "Brown Sugar Oat Milk Tea", "Green Aqua Jasmine Tea"],
        "category": "Boba"
    },
    {
        "id": 7,
        "name": "Té Company",
        "image": "https://s3-media0.fl.yelpcdn.com/bphoto/o035v9_gR-vMj1LfzNBgeQ/o.jpg",
        "description": """Té Company is a specialty tea shop focusing on Taiwanese tea 
        and handmade tea snacks, sourcing directly from small farmers in Taiwan. They 
        offer a curated selection of exquisite teas, including oolong, black, green, white, 
        and herbal teas, alongside unique tea snacks. Their dedication to quality and 
        craftsmanship highlights the rich tea culture of Taiwan, making it a destination 
        for tea enthusiasts looking to explore authentic flavors and tea-making traditions.""",
        "rating": "4.8",
        "address": "163 W 10th St New York, NY 10014",
        "example_drinks": ["Iron Goddess Cold Brew", "Ruby Brew", 
                           "Oriental Beauty Tea", "Pineapple Linzer Tea"],
        "category": "Tea"
    },
    {
        "id": 8,
        "name": "Setsugekka East Village",
        "image": "https://s3-media0.fl.yelpcdn.com/bphoto/z0z-5OxVox034iHFzCWFvQ/o.jpg",
        "description": """Setsugekka, located in the East Village of New York, offers an 
        authentic Japanese tea experience with a focus on matcha and traditional tea 
        ceremonies. This teahouse is a haven for tea lovers, providing lessons on making 
        matcha, along with tea ceremony events. Setsugekka embraces the rich culture of 
        Japanese tea, making it a unique spot for those looking to immerse themselves in 
        the art and tradition of tea drinking.""",
        "rating": "4.7",
        "address": "74 E 7th St New York, NY 10003",
        "example_drinks": ["Hot Matcha", "Hot Matcha-ppuchino", 
                           "Iced Matcha Latte", "Matcha by a tea bowl"],
        "category": "Tea"
    },
    {
        "id": 9,
        "name": "Paquita",
        "image": "https://s3-media0.fl.yelpcdn.com/bphoto/h2nDYxgTJ7_vChZi6ulcWQ/o.jpg",
        "description": """Paquita is a quaint tea room nestled in Manhattan's West Village, 
        offering a warm and inviting atmosphere. This small yet charming spot serves a 
        variety of teas, tisanes, coffee, and baked goods, including gluten-free options. 
        The decor features wooden shelves, copper tea canisters, and a hammered tin ceiling, 
        creating a cozy ambiance. In addition to beverages, Paquita sells teaware, accessories, 
        and artisanal items. The shop, which opened in 2021 by Mariquit Ingalla, pays homage 
        to its historic location and Ingalla's late grandmother, offering over 100 varieties 
        of organic loose tea and botanicals.""",
        "rating": "4.7",
        "address": "242 W 10th St New York, NY 10014",
        "example_drinks": ["Rose Congou", "Lapsang Souchong Magic", 
                           "Iced Berry Tea", "Herbal Tea"],
        "category": "Tea"
    },
    {
        "id": 10,
        "name": "Le Phin",
        "image": "https://s3-media0.fl.yelpcdn.com/bphoto/o035v9_gR-vMj1LfzNBgeQ/o.jpg",
        "description": """Le Phin, nestled in the East Village of New York, is a Vietnamese 
        café that exudes charm and warmth, making it the perfect spot for a coffee break 
        or light bite. The café's owner, Kim Lê, brings her expertise as a coffee quality 
        grader from Vietnam to the table, offering phin-brewed coffee alongside house-made 
        pandan syrup lattes, croissants, blueberry muffins, and scones. The space is cozy 
        and inviting, with white brick walls, light wood furniture, and fresh flowers that 
        fill the room with natural light on sunny days. """,
        "rating": "4.7",
        "address": "259 E 10th St New York, NY 10009",
        "example_drinks": ["Iced Pandan Latte", "Pandan Matcha Latte", 
                           "Vietnamese Iced Coffee", "Phin Brewed Coffee"],
        "category": "Coffee"
    }
    
]

# helper functions

def highlight_matches(text, query):
    """Highlight all case-insensitive matches of query in text."""
    highlighted_text = re.sub(f'(?i)({re.escape(query)})', r'<span class="highlight">\1</span>', text)
    return Markup(highlighted_text)

def is_valid_url(url):
    try:
        result = urlparse(url)
        return all([result.scheme, result.netloc])
    except ValueError:
        return False

# ROUTES

@app.route('/')
def homepage():
   # Filter items by ID
   selected_ids = [1, 5, 9]
   selected_items = [item for item in data if item["id"] in selected_ids]
   return render_template('homepage.html', items=selected_items)

@app.route('/view/<int:item_id>')
def item_info(item_id):
    item = next((item for item in data if item["id"] == item_id), None)
    if item:
        return render_template('view.html', item=item)
    else:
        return "Item not found", 404

@app.route('/search')
def search():
    query = request.args.get('query', '').lower()
    if query:
        matched_items = []
        for item in data:
            item_copy = item.copy()
            # Preprocess and highlight matches in name, description, and category
            for field in ['name', 'category']:
                if field in item_copy:
                    item_copy[field] = highlight_matches(item_copy[field], query)
                    
            # Check if query matches the item's name, description, or category
            if query in item_copy["name"].lower() or query in item_copy.get("category", "").lower():
                item_copy['example_drinks'] = [highlight_matches(drink, query) for drink in item_copy['example_drinks']]
                matched_items.append(item_copy)
            else:
                # Filter example_drinks to include only those that match the query
                matching_drinks = [drink for drink in item_copy.get("example_drinks", []) if query in drink.lower()]
                if matching_drinks:
                    # Create a copy of the item dict to avoid modifying the original data
                    item_copy['example_drinks'] = matching_drinks
                    item_copy['example_drinks'] = [highlight_matches(drink, query) for drink in item_copy['example_drinks']]
                    matched_items.append(item_copy)
        num_results = len(matched_items)
        return render_template('search_results.html', items=matched_items, query=query, num_results=num_results)
    else:
        return render_template('search_results.html', items=[], query="", num_results=0)
    
@app.route('/add', methods=['GET', 'POST'])
def add():
    if request.method == 'POST':
        content = request.get_json()
        errors = {}
        
        # Validate name
        if not content.get('name'):
            errors['name'] = 'Name cannot be blank.'

        # Validate image URL
        if not content.get('image'):
            errors['image'] = 'Image URL cannot be blank.'
        elif not is_valid_url(content['image']):
            errors['image'] = 'Invalid URL format for image.'

        # Validate description
        if not content.get('description'):
            errors['description'] = 'Description cannot be blank.'

        # Validate rating
        try:
            rating = float(content['rating'])
            if not 0 <= rating <= 5:
                errors['rating'] = 'Rating must be between 0 and 5.'
        except (ValueError, TypeError):
            errors['rating'] = 'Rating must be a number.'

        # Validate address
        if not content.get('address'):
            errors['address'] = 'Address cannot be blank.'

        # Validate example_drinks
        if not content.get('example_drinks'):
            errors['example_drinks'] = 'At least one example drink is required.'
        else:
            for drink in content['example_drinks']:
                if not drink:
                    errors['example_drinks'] = 'Example drink names cannot be blank.'
                    break
                
        if errors:
            print("Errors:", errors)  # Print errors to console
            app.logger.error("Errors: %s", errors)  # Log errors
            return jsonify({'errors': errors}), 400

        # Save the data - Replace this with actual database save logic
        new_item_id = len(data) + 1
        content['id'] = new_item_id
        data.append(content)
        return jsonify({'message': 'New item successfully created', 'new_item_id': new_item_id}), 200
    
    else:
        return render_template('add_item.html')

@app.route('/edit/<int:item_id>', methods=['GET', 'POST'])
def edit(item_id):
    item = next((item for item in data if item["id"] == item_id), None)
    if not item:
        return jsonify({'error': 'Item not found'}), 404
    if request.method == 'POST':
        content = request.get_json()
        errors = {}
        
        # Validate name
        if not content.get('name'):
            errors['name'] = 'Name cannot be blank.'

        # Validate image URL
        if not content.get('image'):
            errors['image'] = 'Image URL cannot be blank.'
        elif not is_valid_url(content['image']):
            errors['image'] = 'Invalid URL format for image.'

        # Validate description
        if not content.get('description'):
            errors['description'] = 'Description cannot be blank.'

        # Validate rating
        try:
            rating = float(content['rating'])
            if not 0 <= rating <= 5:
                errors['rating'] = 'Rating must be between 0 and 5.'
        except (ValueError, TypeError):
            errors['rating'] = 'Rating must be a number.'

        # Validate address
        if not content.get('address'):
            errors['address'] = 'Address cannot be blank.'

        # Validate example_drinks
        if not content.get('example_drinks'):
            errors['example_drinks'] = 'At least one example drink is required.'
        else:
            for drink in content['example_drinks']:
                if not drink:
                    errors['example_drinks'] = 'Example drink names cannot be blank.'
                    break
        
        if errors:
            return jsonify({'errors': errors}), 400
        
        item.update({
            "name": content['name'],
            "image": content['image'],
            "description": content['description'],
            "rating": content['rating'],
            "address": content['address'],
            "example_drinks": content['example_drinks']
        })

        return jsonify({'message': 'Item successfully updated'}), 200
    
    else:
        return render_template('edit_item.html', item=item)



if __name__ == '__main__':
   app.run(debug = True)
