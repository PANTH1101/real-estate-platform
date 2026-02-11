from django.db.models import Count, Q
from django.shortcuts import render
from django.views import View
from rest_framework import status
from rest_framework.permissions import IsAdminUser
from rest_framework.response import Response
from rest_framework.views import APIView

from apps.accounts.models import User
from apps.properties.models import Property


class BuyerDashboardView(View):
    template_name = 'dashboard/buyer.html'
    
    def get(self, request):
        return render(request, self.template_name)


class SellerDashboardView(View):
    template_name = 'dashboard/seller.html'
    
    def get(self, request):
        return render(request, self.template_name)


class AdminDashboardView(View):
    template_name = 'dashboard/admin.html'
    
    def get(self, request):
        return render(request, self.template_name)


# API Views for Admin endpoints
class AdminUsersView(APIView):
    permission_classes = [IsAdminUser]
    
    def get(self, request):
        users = User.objects.all().order_by('-created_at')
        data = {
            'results': [
                {
                    'id': str(u.id),
                    'email': u.email,
                    'full_name': u.full_name,
                    'phone_number': u.phone_number,
                    'role': u.role,
                    'is_active': u.is_active,
                    'is_email_verified': u.is_email_verified,
                    'created_at': u.created_at.isoformat(),
                }
                for u in users
            ],
            'count': users.count(),
        }
        return Response(data)


class AdminAnalyticsView(APIView):
    permission_classes = [IsAdminUser]
    
    def get(self, request):
        total_users = User.objects.count()
        total_properties = Property.objects.count()
        approved_properties = Property.objects.filter(is_approved=True).count()
        pending_properties = Property.objects.filter(is_approved=False).count()
        
        # Properties by city
        properties_by_city = (
            Property.objects.values('city')
            .annotate(count=Count('id'))
            .order_by('-count')[:10]
        )
        
        # Total enquiries
        from apps.enquiries.models import Enquiry
        total_enquiries = Enquiry.objects.count()
        
        data = {
            'total_users': total_users,
            'total_properties': total_properties,
            'approved_properties': approved_properties,
            'pending_properties': pending_properties,
            'total_enquiries': total_enquiries,
            'properties_by_city': list(properties_by_city),
        }
        return Response(data)
