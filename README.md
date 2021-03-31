# customer-support-application

### This app implements the following functionalities

### Customer Enquiry</br>
<ul>
    <li>
        The customer visits the 'Enquiry Form' url and fills his name, phone number, email id and query.
    </li>
    <li>
        The Enquiry form data is stored in database and an email with the url to view and reply to the enquiry is sent to the service provider
    </li>
    <li>
        Service Providers can be added or deleted from the 'Manage Service Providers' page. Each service provider has its own url for enquiry form
    </li>
</ul> 

### Service Provider Feedback</br>
<ul>
    <li>
        The url points to the 'Response Form' which contains customer enquiry details with a response text box field.
    </li>
    <li>
        The response, submitted by the service provider, is stored in the database against the customer enquiry and sent to the customer.
    </li>
</ul>

### Customer Review</br>
<ul>
    <li>
        After 60 minutes an email is sent to the customer with url for 'Review Form'. The rating is binary i.e. 'satisfied' or 'unsatisfied'
    </li>
    <li>
        The submitted review is recorde against the customer enquiry. The url has a validity of 30 minutes.
    </li>
</ul>
</br>

### To view a demo of the app please visit the following link
<a href="https://drive.google.com/file/d/1tPgOtXxiJiXoL0DpgkR5qfmCPeYq6nWS/view?usp=sharing">Demo Video</a></br></br>

### Notes:-
<ul>
    <li>
        For demo python's built-in local smtp server has been used, the email, with details, are printed on the terminal.
    </li>
    <li>
        Public email hosts, such as google's gmail, can be added in the settings.py file.</br>
        <a>https://stackoverflow.com/questions/31324005/django-1-8-sending-mail-using-gmail-smtp</a>
    </li>
</ul>

<br>

### Author
__[Nooh Shaikh](https://github.com/n37hk)__</br>
nshaikh304@gmail.com