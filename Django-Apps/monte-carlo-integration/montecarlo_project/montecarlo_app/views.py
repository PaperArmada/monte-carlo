import numpy as np
import matplotlib
matplotlib.use('Agg')  # Use a non-interactive backend
import matplotlib.pyplot as plt
from django.shortcuts import render
from django import forms
import base64
from io import BytesIO

# Define the form
class MonteCarloForm(forms.Form):
    a = forms.FloatField(label='Lower Bound (a)', initial=0)
    b = forms.FloatField(label='Upper Bound (b)', initial=np.pi)
    num_samples = forms.IntegerField(label='Number of Samples', initial=10_000, min_value=1, max_value=1_000_000)

def monte_carlo_integration_visual(f, a, b, num_samples):
    x_random = np.random.uniform(a, b, num_samples)
    y_random = np.random.uniform(0, 1, num_samples)
    f_random = f(x_random)
    points_below_curve = y_random <= f_random
    area_rectangle = (b - a) * 1
    integral_estimate = area_rectangle * np.sum(points_below_curve) / num_samples

    # Visualization
    x = np.linspace(a, b, 500)
    y = f(x)

    plt.figure(figsize=(10, 6))
    plt.plot(x, y, 'r', linewidth=2, label='f(x)')
    plt.fill_between(x, y, alpha=0.2, color='red')

    plt.scatter(x_random[points_below_curve], y_random[points_below_curve],
                color='green', s=1, label='Points Below Curve')
    plt.scatter(x_random[~points_below_curve], y_random[~points_below_curve],
                color='blue', s=1, label='Points Above Curve')

    plt.title('Monte Carlo Integration Visualization')
    plt.xlabel('x')
    plt.ylabel('y')
    plt.legend()

    # Save the plot to a PNG image in memory
    buffer = BytesIO()
    plt.savefig(buffer, format='png')
    plt.close()
    buffer.seek(0)
    image_png = buffer.getvalue()
    buffer.close()

    # Encode the image to base64 to render it in HTML
    graphic = base64.b64encode(image_png)
    graphic = graphic.decode('utf-8')

    return integral_estimate, graphic

def f(x):
    return np.sin(x)

def monte_carlo_view(request):
    if request.method == 'POST':
        form = MonteCarloForm(request.POST)
        if form.is_valid():
            a = form.cleaned_data['a']
            b = form.cleaned_data['b']
            num_samples = form.cleaned_data['num_samples']

            integral_estimate, graphic = monte_carlo_integration_visual(f, a, b, num_samples)

            context = {
                'form': form,
                'integral_estimate': integral_estimate,
                'graphic': graphic,
            }
            return render(request, 'montecarlo_app/result.html', context)
    else:
        form = MonteCarloForm()

    return render(request, 'montecarlo_app/index.html', {'form': form})
