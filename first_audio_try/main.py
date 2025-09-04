import numpy as np
import sounddevice as sd

def white_noise(duration: float=1.0,
                amplitude: float=0.5,
                sample_rate: int=44100
                )->np.ndarray:
    """
    Generate white noise
    """
    # Calculate the number of samples needed
    n_samples = int(duration*sample_rate)

    # Generate white noise with values between -1 and 1
    noise = np.random.uniform(-1,1,n_samples)

    # Scale by amplitude
    noise *= amplitude
    return noise

def main():

    # Generate and play a sound
    mysound = sine_tone()
    sd.play(mysound)
    sd.wait()

def sine_tone(
        frequency: int=440,
        duration: float=6.0,
        amplitude: float=3.0,
        sample_rate: int=44100

)-> np.ndarray:
    """
    Generate a sine tone
    """
    n_samples  =int(sample_rate* duration)

    time_points = np.linspace(0,duration,n_samples, False)
    
    sine = np.sin(2 * np.pi * frequency * time_points)

    sine *= amplitude
    return sine

if __name__ == "__main__":
    main()


# import speechrecognition as sr