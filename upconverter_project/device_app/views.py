from django.shortcuts import render, redirect
from .models import Device, DeviceLog
from django.contrib.auth.decorators import login_required, user_passes_test
from .tcp_client import set_frequency, set_gain, set_mute, set_frequency_step, connect_device, connection
import traceback
from django.core.cache import cache
from django.urls import reverse
from django.http import JsonResponse


@login_required
def device_status_view(request):
    # Check if device is connected
    #is_connected = connection # Function to check if device is connected

    #if not is_connected:
        #context = {'device': None, 'error': 'Device is inactive'}
        #return render(request, 'device_app/status.html', context)

    # Fetch device status if connected
    device = Device.objects.first()
    context = {'device': device, 'error': None}
    return render(request, 'device_app/status.html', context)

@login_required
@user_passes_test(lambda u: u.is_superuser)
def edit_device_view(request):
    device = Device.objects.first()

    if request.method == "POST":
        # Process POST data here if needed
        return redirect('edit_device')

    context = {
        'frequency': device.frequency,
        'frequency_step': device.frequency_step,
        'gain': device.gain,
        'mute': device.mute,
    }
    return render(request, 'device_app/edit.html', context)

@login_required
@user_passes_test(lambda u: u.is_superuser)
def edit_frequency_view(request):
    if request.method == 'POST':
        frequency = request.POST.get('frequency')
        try:
            device = Device.objects.get(id=1)  # Use 'id' instead of 'PK'
            
            if device.frequency != frequency:
                response = set_frequency(frequency)  # Call the set_frequency function from tcp_client
                
                if response:
                    # Update Device table
                    device.frequency = frequency
                    device.save()
                    DeviceLog.objects.create(user=request.user, action="Frequency Change", status="Success", details=f"Frequency set to {frequency} MHz")
                    return render(request, 'device_app/edit.html', {'success': f"Frequency updated to {frequency} MHz", 'frequency': device.frequency, 'frequency_step': device.frequency_step, 'gain': device.gain, 'mute': device.mute})
                else:
                    DeviceLog.objects.create(user=request.user, action="Frequency Change", status="Failure", details=f"Failed to set frequency to {frequency} MHz")
                    return render(request, 'device_app/edit.html', {'error': "Failed to update frequency", 'frequency': device.frequency, 'frequency_step': device.frequency_step, 'gain': device.gain, 'mute': device.mute})
            else:
                return render(request, 'device_app/edit.html', {'info': "Frequency is already set to the current value"})
        except Device.DoesNotExist:
            return render(request, 'device_app/edit.html', {'error': "Device not found", 'frequency': device.frequency, 'frequency_step': device.frequency_step, 'gain': device.gain, 'mute': device.mute})
    
    return redirect('edit_device')


@login_required
@user_passes_test(lambda u: u.is_superuser)
def edit_frequency_step_view(request):
    if request.method == 'POST':
        frequency_step = request.POST.get('frequency_step')
        try:
            device = Device.objects.get(id=1)  # Use 'id' instead of 'PK'
            
            if device.frequency_step != frequency_step:
                response = set_frequency_step(frequency_step)  # Call the set_frequency_step function from tcp_client
                
                if response:
                    # Update Device table
                    device.frequency_step = frequency_step
                    device.save()
                    DeviceLog.objects.create(user=request.user, action="Frequency Step Change", status="Success", details=f"Frequency step set to {frequency_step} Hz")
                    return render(request, 'device_app/edit.html', {'success': f"Frequency step updated to {frequency_step} Hz"})
                else:
                    DeviceLog.objects.create(user=request.user, action="Frequency Step Change", status="Failure", details=f"Failed to set frequency step to {frequency_step} Hz")
                    return render(request, 'device_app/edit.html', {'error': "Failed to update frequency step"})
            else:
                return render(request, 'device_app/edit.html', {'info': "Frequency step is already set to the current value"})
        except Device.DoesNotExist:
            return render(request, 'device_app/edit.html', {'error': "Device not found"})
    
    return redirect('edit_device')


@login_required
@user_passes_test(lambda u: u.is_superuser)
def edit_gain_view(request):
    if request.method == 'POST':
        gain_str = request.POST.get('gain')
        
        try:
            gain = int(gain_str)  # Convert gain to a float for numerical comparison
            device = Device.objects.get(id=1)  # Use 'id' instead of 'PK'
            
            if device.gain != gain:
                response = set_gain(gain)  # Call the set_gain function from tcp_client
                
                if response:
                    # Update Device table
                    device.gain = gain
                    device.save()
                    DeviceLog.objects.create(user=request.user, action="Gain Change", status="Success", details=f"Gain set to {gain} dB")
                    return render(request, 'device_app/edit.html', {'success': f"Gain updated to {gain} dB"})
                else:
                    DeviceLog.objects.create(user=request.user, action="Gain Change", status="Failure", details=f"Failed to set gain to {gain} dB")
                    return render(request, 'device_app/edit.html', {'error': "Failed to update gain"})
            else:
                return render(request, 'device_app/edit.html', {'info': "Gain is already set to the current value"})
        except Device.DoesNotExist:
            return render(request, 'device_app/edit.html', {'error': "Device not found"})
        except ValueError:
            return render(request, 'device_app/edit.html', {'error': "Invalid gain value"})
    
    return redirect('edit_device')


@login_required
@user_passes_test(lambda u: u.is_superuser)
def edit_mute_view(request):
    if request.method == 'POST':
        mute = request.POST.get('mute')
        try:
            device = Device.objects.get(id=1)  # Use 'id' instead of 'PK'
            
            if device.mute != mute:
                response = set_mute(mute)  # Call the set_mute function from tcp_client
                
                if response:
                    # Update Device table
                    device.mute = mute
                    device.save()
                    DeviceLog.objects.create(user=request.user, action="Mute Change", status="Success", details=f"Mute set to {mute}")
                    return render(request, 'device_app/edit.html', {'success': f"Mute updated to {mute}"})
                else:
                    DeviceLog.objects.create(user=request.user, action="Mute Change", status="Failure", details=f"Failed to set mute to {mute}")
                    return render(request, 'device_app/edit.html', {'error': "Failed to update mute"})
            else:
                return render(request, 'device_app/edit.html', {'info': "Mute is already set to the current value"})
        except Device.DoesNotExist:
            return render(request, 'device_app/edit.html', {'error': "Device not found"})
    
    return redirect('edit_device')

@login_required
def logs_view(request):
    logs = DeviceLog.objects.all().order_by('-timestamp')  # Get all logs ordered by timestamp (latest first)
    return render(request, 'device_app/logs.html', {'logs': logs})

@login_required
def get_device_alerts(request):
    if cache.get('device_disconnected'):
        # Redirect to the sign-in page if device is disconnected
        return redirect(reverse('login'))
    alerts = cache.get('device_alerts', [])
    return JsonResponse({'alerts': alerts})
