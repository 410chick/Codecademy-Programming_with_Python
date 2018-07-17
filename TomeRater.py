
"""
    TomeRater class handles the interface for users of the TomeRater
    book rating system.  This class manages the majority of methods used
    to add books, users, and ratings and also manages the analysis of 
    these items.  It uses dictionaries of book ojects and a dictionary of 
    User objects to manage the details assosiated wth both.

        users - a dictionary of format {email: User}
        books - a dictionary of format {Book: num_users_read}
"""
class TomeRater():
    def __init__(self):
        self.users = {}
        self.books = {}


    ### Create a new User object and add assosiated Book objects to the user profile
    def add_user(self, name, email, user_books=[]):
        self.users[email] = User(name, email)

        for book in user_books:
            self.add_book_to_user(book, email)


    ### Create a new Book object
    def create_book(self, title, isbn):
        return(Book(title, isbn))


    ### Create a new Fiction object (type of Book)
    def create_novel(self, title, author, isbn):
        return(Fiction(title, author, isbn))


    ### Create a new Non_Fiction object (type of Book)
    def create_non_fiction(self, title, subject, level, isbn):
        return(Non_Fiction(title, subject, level, isbn))


    ### Adds a Book object to a User. Adds ratings, if specified, to the Book and User
    def add_book_to_user(self, book, email, rating=None):
        if email in self.users:
            user = self.users[email]
        else:
            print("No user with email {}!".format(email))
            return()

        user.read_book(book, rating)
        if rating:
            book.add_rating(rating)

        if book in self.books:
            self.books[book] = self.books[book] + 1
        else:
            self.books[book] = 1


    """ 
        ANALYSIS METHODS HERE
    """

    ### print the entire catalog of books
    def print_catalog(self):
        print("\nTomeRater Current Catalog of Books")
        [print("\t{}".format(book)) for book in self.books.keys()]


    ### print all the users of the system
    def print_users(self):
        print("\nTomeRater Current List of Users")
        [print("\t{}".format(user)) for user in self.users.keys()]


    ### get list of most read book. Array returned since multiple books could have the 
    ###   max number of reads.  
    def get_most_read_book(self):

        max_read = max(self.books.values())

        max_read_books = []

        for book, times_read in self.books.items():
            if (times_read == max_read):
                max_read_books.append(book)

        return(max_read_books)


    ### return the highest rated book.  This uses all the ratings from users
    ###   returns a list since multiple books could have the same rating
    def highest_rated_book(self):

        max_rated_book = []

        max_rating = max([book.get_average_rating() for book in self.books.keys()])

        for book in self.books.keys():
            if book.get_average_rating() == max_rating:
                max_rated_book.append(book)

        return(max_rated_book)


    ### returns the user who consistantly rates books the hightest. 
    ###   returns a list since multple users can equally lack the ability 
    ###   to properly rate what they read
    def most_positive_user(self):

        most_positive_users= []

        max_rating = max([user.get_average_rating() for user in self.users.values()])

        for user in self.users.values():
            if user.get_average_rating() == max_rating:
                most_positive_users.append(user)

        return(most_positive_users)

"""
    User class handles the attribues assosiated with the system

        name - a string wth the users name
        email - a string with the users email
        books - a dictionary of format {Book: rating}
"""
class User():
    def __init__(self, name, email):
        self.name = name
        self.email = email
        self.books = {}


    ### returns the current eamil address for the user
    def get_email(self):
        return(self.email)


    ### allows the user to change their eamil address
    def change_email(self, address):
        self.email = address 


    ### records when a book is read and adds the rating
    def read_book(self, book, rating=None):
        self.books[book] = rating


    ### returns the average rating for a given user 
    def get_average_rating(self):
        try:
            return(sum({value for (key, value) in self.books.items() if value != None})/float(len(self.books)))

        except ZeroDivisionError:
            return (0)


    ### reports all the current inforamtion for the user when the object is printed
    def __repr__(self):
        if len(self.books) > 0:
            return("{}, email {}, has read {} books.".format(self.name, self.email, str(len(self.books))))
        else:
            return("{}, email {}, has not read any books yet.".format(self.name, self.email))


    ### a way of insuring the same user isn't defined twice
    def __eq__(self, other_user):
        if (self.name == other_user.name) & (self.email == other_user.email):
            return(TRUE)
        else:
            return(FALSE)


""" 
    Book class manages the attributes for each book.  The creation of a book object 
    will create that book.  Users may get inforamtion about the book, add a rating 
    for the book, or view comparisons of books

        title - a string wth the title of the book
        isbn - a string with the isbn of the book
        books - a list of Book objects
"""
class Book():
    def __init__(self, title, isbn):
        self.title = title
        self.isbn = isbn
        self.ratings=[]


    ### avoids hash errors from using the book dictionary as a hash key
    def __hash__(self):
        return hash((self.title, self.isbn))

    ### All the book getters!
    def get_title(self):
        return(self.title)
    def get_isbn(self):
        return(self.isbn)


    ### to change the isbn number after the book was created... Somebody got it wrong?
    def set_isbn(self, isbn):
        print("Somebody messed up\n\tchanging ISBN from {} to {}".format(str(self.isbn), isbn))
        self.isbn = isbn

    ### add rating to the book
    def add_rating(self, rating):
        if 0 <= rating <= 4:
            self.ratings.append(rating)
                                        
        else:
            print ("Rating of {} not valid".format(str(rating)))


    ### returns the average rating for a given book
    def get_average_rating(self):
        return(sum([num for num in self.ratings])/float(len(self.ratings)))


    ### prints the attributes of the book when the Book object is printed
    def __repr__(self):
        return("{} with isbn {}".format(self.title, self.isbn))

    ### a way of insuring the same book isn't defined twice
    def __eq__ (self, other_book):
        if (self.isbn == other_book.isbn) & (self.title == otehr_book.title):
            return(TRUE)
        else:
            return(FALSE)


""" 
    Fiction class manages the attributes for each book.  The creation of a Fiction object 
    will create that book.  Users may get inforamtion about the book, add a rating 
    for the book, or view comparisons of books

        title - a string wth the title of the book
        isbn - a string with the isbn of the book
        author - a string with the authors name
        books - a list of Book objects
"""
class Fiction(Book):
    def __init__(self, title, author, isbn):
        super().__init__(title, isbn)
        self.author = author


    ### All the book getters!
    def get_author(self):
        return(self.author)


    ### prints the attributes of the book when the Ficton object is printed
    def __repr__(self):
        return("{} by {}".format(self.title, self.author))


""" 
    Non_Fiction class manages the attributes for each book.  The creation of a 
    Non_Fiction object will create that book.  Users may get inforamtion about 
    the book, add a rating for the book, or view comparisons of books

        title - a string wth the title of the book
        isbn - a string with the isbn of the book
        subject - a string with the subject of the book
        level - the level of the subject (beginner, intermediate, advanced)
        books - a list of Book objects
"""
class Non_Fiction(Book):
    
    def __init__(self, title, subject, level, isbn):
        super().__init__(title, isbn)
        self.subject = subject
        self.level = level


    ### All the book getters!
    def get_subject(self):
        return(self.subject)
    def get_level(self):
        return(self.level)


    ### prints the attributes of the book when the Non_Fiction object is printed
    def __repr__(self):
        if (self.level[0].lower() == "a"):
            return("{}, an {} manual on {}".format(self.title, self.level, self.subject))
        else:
            return("{}, a {} manual on {}".format(self.title, self.level, self.subject))


