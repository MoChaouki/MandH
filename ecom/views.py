from django.http import HttpResponse


def payment_completed_view(request):
    return HttpResponse("Payment completed successfully!")

def payment_failed_view(request):
    return HttpResponse("Payment failed!")

