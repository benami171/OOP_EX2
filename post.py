import matplotlib.pyplot as plt
import matplotlib.image as mpimg
from Observer import Sender

# Factory method to create different types of posts.

class PostFactory:
    @staticmethod
    def create_post(post_type, *args, **kwargs):
        # Factory method to create different types of posts.
        if post_type == "Text":
            return TextPost(*args, **kwargs)
        elif post_type == "Image":
            return ImagePost(*args, **kwargs)
        elif post_type == "Sale":
            return SalePost(*args, **kwargs)
        else:
            raise ValueError("Invalid post type")

# Abstract class for different types of posts.
# The class inherits from the Sender class, which is an observer pattern.
class Post(Sender):
    def __init__(self, user, post_type, *args, **kwargs):
        # Initialize a new post.
        super().__init__()
        self.user = user
        self.post_type = post_type

    def like(self, user):
        if user.logged_in is False:
            raise PermissionError("User is not logged in.")
        if user != self.user:
            print(f"notification to {self.user.username}: {user.username} liked your post")
            self.notify(user, self.user, "like")
        return True

    def comment(self, user, comment):
        if user.logged_in is False:
            raise PermissionError("User is not logged in.")
        if user != self.user:
            print(f"notification to {self.user.username}: {user.username} commented on your post: {comment}")
            self.notify(user, self.user, "comment")
        return True

    def __str__(self):
        pass

# All the different types of posts inherit from the Post class.

class TextPost(Post):
    def __init__(self, user, content):
        # Initialize a new text post.
        super().__init__(user, "Text")
        self.content = content

    def __str__(self):
        return f'{self.user.username} published a post:\n"{self.content}"\n'


class ImagePost(Post):
    def __init__(self, user, image_path):
        # Initialize a new image post.
        super().__init__(user, "Image")
        self.image_path = image_path

    def display(self):
        try:
            img = mpimg.imread(self.image_path)
            plt.imshow(img)
            plt.axis('off')
            plt.show()
            print("Shows picture")
        except FileNotFoundError:
            print("Image not found.")

    def __str__(self):
        return f"{self.user.username} posted a picture\n"


class SalePost(Post):
    def __init__(self, user, product_description, price, pickup_location):
        # Initialize a new sale post.
        super().__init__(user, "Sale")
        self.product_description = product_description
        self.price = price
        self.pickup_location = pickup_location
        self.available = True

    def discount(self, percentage, password):
        if self.user.logged_in is False:
            raise PermissionError("User is not logged in.")
        if self.user.password == password:
            self.price *= (100 - percentage) / 100
            print(f"Discount on {self.user.username} product! the new price is: {self.price}")
        else:
            print("Incorrect password. Discount cannot be applied.")

    def sold(self, password):
        if self.user.logged_in is False:
            raise PermissionError("User is not logged in.")
        if self.user.password == password:
            self.available = False
            print(f"{self.user.username}'s product is sold")
        else:
            print("Incorrect password. Product cannot be marked as sold.")

    def __str__(self):
        status = "For sale!" if self.available else "Sold!"
        return (f"{self.user.username} posted a product for sale:\n{status} {self.product_description},"
                f" price: {self.price}, pickup from: {self.pickup_location}\n")
