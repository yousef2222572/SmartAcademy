# SmartAcademy
# Academy Platform

An educational platform where users can study courses and lessons, purchase courses individually, ask other users questions about topics they do not understand, and use an AI assistant with the Pro plan.

 <a href="https://nondetrimental-nell-hesitantly.ngrok-free.dev/">try demo</a>

## Main Features

* Browse and study available courses and lessons.
* Purchase individual courses without requiring a subscription.
* Pro users can access all available courses without purchasing them individually.
* AI assistant available to Pro users for learning and understanding course material.
* Users can ask questions and discuss topics they do not understand.
* User accounts and authentication.
* Course and user permission management.
* Payment processing through Stripe.
* Stripe webhooks for confirming successful payments and updating user course permissions.

## Technology Stack

* **Backend:** Django
* **Language:** Python
* **Database:** SQLite
* **Frontend:** HTML, CSS, JavaScript
* **Payments:** Stripe
* **Development:** Django development server
* **Webhook testing:** Stripe CLI / ngrok

## Running the Project Locally

1. Clone the project.
2. Create and activate a Python virtual environment.
3. Install the required dependencies:

```bash
pip install -r requirements.txt
```

4. Run database migrations:

```bash
python manage.py migrate
```

5. Start the Django development server:

```bash
python manage.py runserver
```

The project will then be available locally at:

```text
http://127.0.0.1:8000/
```

## Stripe Webhook

The project uses Stripe webhooks to process payment events after a successful checkout.

During local development, Stripe CLI can forward webhook events directly to the Django application:

```bash
stripe listen --forward-to http://localhost:8000/checkout/stripe/webhook/
```

The webhook endpoint is:

```text
/checkout/stripe/webhook/
```

After receiving a successful payment event, the application processes the transaction and grants the user access to the purchased course.

## Project Structure

The project is divided into Django applications according to their responsibilities. The main components include:

* `accounts` — user accounts and authentication.
* `academy_core` — core academy functionality and courses.
* `ai_chat` — AI assistant functionality.
* `article_app` — articles and educational content.
* `checkout` — payments, transactions, and Stripe webhook handling.

The main Django project configuration is located in:

```text
academy_project/
```

## Published Version

**Live website:**


## Development Status

The platform is currently under active development. The core academy, course purchasing, user permissions, Stripe payments, and AI functionality are being developed and tested, with additional social and course-management features planned for future versions.
