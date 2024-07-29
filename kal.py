import numpy as np

class KalmanFilter:
    def __init__(self):
        # Initial state (location and velocity)
        self.state = np.array([[0], [0], [0], [0]], dtype='float64')
        
        # State transition matrix
        self.A = np.array([[1, 0, 1, 0],
                           [0, 1, 0, 1],
                           [0, 0, 1, 0],
                           [0, 0, 0, 1]], dtype='float64')
        
        # Measurement matrix
        self.H = np.array([[1, 0, 0, 0],
                           [0, 1, 0, 0]], dtype='float64')
        
        # Process noise covariance
        self.Q = np.eye(self.A.shape[1], dtype='float64') * 0.01
        
        # Measurement noise covariance
        self.R = np.eye(self.H.shape[1], dtype='float64') * 0.1
        
        # Error covariance matrix
        self.P = np.eye(self.A.shape[1], dtype='float64')
        
    def predict(self, x, y):
        # Update state
        self.state = self.A.dot(self.state)
        
        # Update error covariance
        self.P = self.A.dot(self.P).dot(self.A.T) + self.Q
        
        # Measurement
        Z = np.array([[x], [y]], dtype='float64')
        
        # Kalman gain
        S = self.H.dot(self.P).dot(self.H.T) + self.R
        K = self.P.dot(self.H.T).dot(np.linalg.inv(S))
        
        # Update state with measurement
        self.state = self.state + K.dot(Z - self.H.dot(self.state))
        
        # Update error covariance
        I = np.eye(self.A.shape[1], dtype='float64')
        self.P = (I - K.dot(self.H)).dot(self.P)
        
        return int(self.state[0][0]), int(self.state[1][0])
