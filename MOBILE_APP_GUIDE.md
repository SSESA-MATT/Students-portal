# 📱 Mobile App Development Guide - Student Portal

## 🎯 Overview

Build a cross-platform mobile app for the Student Portal using **React Native + Expo**. This guide provides complete setup and implementation.

---

## 🚀 Quick Start

### Prerequisites
- Node.js 18+ installed
- npm or yarn
- Expo Go app on your phone (for testing)
- Your API deployed or running locally

### Create New React Native Project

```bash
# Create new Expo app
npx create-expo-app@latest StudentPortalApp

cd StudentPortalApp

# Install dependencies
npm install axios @react-navigation/native @react-navigation/native-stack
npm install react-native-screens react-native-safe-area-context
npm install @react-native-async-storage/async-storage
npm install react-native-vector-icons
```

---

## 📂 Project Structure

```
StudentPortalApp/
├── app/
│   ├── (auth)/
│   │   ├── login.js
│   │   └── register.js
│   ├── (tabs)/
│   │   ├── _layout.js
│   │   ├── index.js          # Dashboard
│   │   ├── courses.js
│   │   ├── grades.js
│   │   └── profile.js
│   └── _layout.js
├── components/
│   ├── CourseCard.js
│   ├── GradeItem.js
│   ├── ReviewModal.js
│   └── LoadingSpinner.js
├── services/
│   ├── api.js                # API client
│   ├── auth.js               # Auth service
│   └── storage.js            # AsyncStorage wrapper
├── constants/
│   ├── Colors.js
│   └── config.js
├── hooks/
│   └── useAuth.js
└── package.json
```

---

## 🔧 Configuration

### 1. Create API Configuration

Create `constants/config.js`:
```javascript
// For local development, use your computer's IP (not localhost)
// Find your IP: ipconfig (Windows) or ifconfig (Mac/Linux)
const API_BASE_URL = __DEV__
  ? 'http://192.168.1.100:8000/api'  // Replace with your IP
  : 'https://student-portal-api.onrender.com/api';

export const config = {
  apiUrl: API_BASE_URL,
  tokenRefreshInterval: 60 * 60 * 1000, // 1 hour
  requestTimeout: 30000, // 30 seconds
};

export default config;
```

### 2. Create API Client

Create `services/api.js`:
```javascript
import axios from 'axios';
import AsyncStorage from '@react-native-async-storage/async-storage';
import { config } from '../constants/config';

const api = axios.create({
  baseURL: config.apiUrl,
  timeout: config.requestTimeout,
  headers: {
    'Content-Type': 'application/json',
  },
});

// Request interceptor - Add JWT token to requests
api.interceptors.request.use(
  async (config) => {
    const token = await AsyncStorage.getItem('accessToken');
    if (token) {
      config.headers.Authorization = `Bearer ${token}`;
    }
    return config;
  },
  (error) => {
    return Promise.reject(error);
  }
);

// Response interceptor - Handle token refresh
api.interceptors.response.use(
  (response) => response,
  async (error) => {
    const originalRequest = error.config;

    // If 401 and not already retried
    if (error.response?.status === 401 && !originalRequest._retry) {
      originalRequest._retry = true;

      try {
        const refreshToken = await AsyncStorage.getItem('refreshToken');
        const response = await axios.post(
          `${config.apiUrl}/auth/refresh/`,
          { refresh: refreshToken }
        );

        const { access } = response.data;
        await AsyncStorage.setItem('accessToken', access);

        // Retry original request with new token
        originalRequest.headers.Authorization = `Bearer ${access}`;
        return api(originalRequest);
      } catch (refreshError) {
        // Refresh failed - logout user
        await AsyncStorage.multiRemove(['accessToken', 'refreshToken', 'userProfile']);
        // Navigate to login screen (implement based on your navigation)
        return Promise.reject(refreshError);
      }
    }

    return Promise.reject(error);
  }
);

export default api;
```

### 3. Create Auth Service

Create `services/auth.js`:
```javascript
import AsyncStorage from '@react-native-async-storage/async-storage';
import api from './api';

export const authService = {
  // Login
  async login(username, password) {
    try {
      const response = await api.post('/auth/login/', {
        username,
        password,
      });

      const { access, refresh } = response.data;
      
      // Store tokens
      await AsyncStorage.setItem('accessToken', access);
      await AsyncStorage.setItem('refreshToken', refresh);

      // Fetch and store user profile
      const profile = await this.getCurrentUser();
      await AsyncStorage.setItem('userProfile', JSON.stringify(profile));

      return { success: true, user: profile };
    } catch (error) {
      return {
        success: false,
        error: error.response?.data?.detail || 'Login failed',
      };
    }
  },

  // Get current user profile
  async getCurrentUser() {
    const response = await api.get('/students/me/');
    return response.data;
  },

  // Logout
  async logout() {
    await AsyncStorage.multiRemove([
      'accessToken',
      'refreshToken',
      'userProfile',
    ]);
  },

  // Check if user is authenticated
  async isAuthenticated() {
    const token = await AsyncStorage.getItem('accessToken');
    return !!token;
  },

  // Get stored user profile
  async getStoredProfile() {
    const profile = await AsyncStorage.getItem('userProfile');
    return profile ? JSON.parse(profile) : null;
  },
};

export default authService;
```

### 4. Create Student API Service

Create `services/students.js`:
```javascript
import api from './api';

export const studentsService = {
  // Get current student details
  async getMe() {
    const response = await api.get('/students/me/');
    return response.data;
  },

  // Get student grades
  async getGrades(studentId) {
    const response = await api.get(`/students/${studentId}/grades/`);
    return response.data;
  },

  // Get student GPA/CGPA
  async getGPA(studentId) {
    const response = await api.get(`/students/${studentId}/gpa/`);
    return response.data;
  },

  // Enroll in course
  async enrollCourse(studentId, courseId) {
    const response = await api.post(`/students/${studentId}/enroll/`, {
      course_id: courseId,
    });
    return response.data;
  },

  // Unenroll from course
  async unenrollCourse(studentId, courseId) {
    const response = await api.post(`/students/${studentId}/unenroll/`, {
      course_id: courseId,
    });
    return response.data;
  },
};

export default studentsService;
```

### 5. Create Courses API Service

Create `services/courses.js`:
```javascript
import api from './api';

export const coursesService = {
  // Get all courses
  async getCourses(params = {}) {
    const response = await api.get('/courses/', { params });
    return response.data;
  },

  // Get course details
  async getCourse(courseId) {
    const response = await api.get(`/courses/${courseId}/`);
    return response.data;
  },

  // Get course reviews
  async getCourseReviews(courseId) {
    const response = await api.get(`/courses/${courseId}/reviews/`);
    return response.data;
  },

  // Submit course review
  async submitReview(courseId, rating, comment) {
    const response = await api.post('/reviews/', {
      course: courseId,
      rating,
      comment,
    });
    return response.data;
  },

  // Update review
  async updateReview(reviewId, rating, comment) {
    const response = await api.put(`/reviews/${reviewId}/`, {
      rating,
      comment,
    });
    return response.data;
  },
};

export default coursesService;
```

---

## 🎨 UI Components

### Login Screen

Create `app/(auth)/login.js`:
```javascript
import React, { useState } from 'react';
import {
  View,
  Text,
  TextInput,
  TouchableOpacity,
  StyleSheet,
  Alert,
  ActivityIndicator,
} from 'react-native';
import { useRouter } from 'expo-router';
import authService from '../../services/auth';

export default function LoginScreen() {
  const [username, setUsername] = useState('');
  const [password, setPassword] = useState('');
  const [loading, setLoading] = useState(false);
  const router = useRouter();

  const handleLogin = async () => {
    if (!username || !password) {
      Alert.alert('Error', 'Please enter username and password');
      return;
    }

    setLoading(true);
    const result = await authService.login(username, password);
    setLoading(false);

    if (result.success) {
      router.replace('/(tabs)');
    } else {
      Alert.alert('Login Failed', result.error);
    }
  };

  return (
    <View style={styles.container}>
      <Text style={styles.title}>Student Portal</Text>
      <Text style={styles.subtitle}>Login to your account</Text>

      <TextInput
        style={styles.input}
        placeholder="Username"
        value={username}
        onChangeText={setUsername}
        autoCapitalize="none"
        autoCorrect={false}
      />

      <TextInput
        style={styles.input}
        placeholder="Password"
        value={password}
        onChangeText={setPassword}
        secureTextEntry
        autoCapitalize="none"
      />

      <TouchableOpacity
        style={styles.button}
        onPress={handleLogin}
        disabled={loading}
      >
        {loading ? (
          <ActivityIndicator color="#fff" />
        ) : (
          <Text style={styles.buttonText}>Login</Text>
        )}
      </TouchableOpacity>
    </View>
  );
}

const styles = StyleSheet.create({
  container: {
    flex: 1,
    justifyContent: 'center',
    padding: 20,
    backgroundColor: '#f5f5f5',
  },
  title: {
    fontSize: 32,
    fontWeight: 'bold',
    textAlign: 'center',
    marginBottom: 10,
    color: '#2196F3',
  },
  subtitle: {
    fontSize: 16,
    textAlign: 'center',
    marginBottom: 40,
    color: '#666',
  },
  input: {
    backgroundColor: '#fff',
    padding: 15,
    borderRadius: 10,
    marginBottom: 15,
    fontSize: 16,
    borderWidth: 1,
    borderColor: '#ddd',
  },
  button: {
    backgroundColor: '#2196F3',
    padding: 15,
    borderRadius: 10,
    alignItems: 'center',
    marginTop: 10,
  },
  buttonText: {
    color: '#fff',
    fontSize: 18,
    fontWeight: 'bold',
  },
});
```

### Dashboard Screen

Create `app/(tabs)/index.js`:
```javascript
import React, { useState, useEffect } from 'react';
import {
  View,
  Text,
  StyleSheet,
  ScrollView,
  RefreshControl,
  ActivityIndicator,
} from 'react-native';
import studentsService from '../../services/students';

export default function DashboardScreen() {
  const [loading, setLoading] = useState(true);
  const [refreshing, setRefreshing] = useState(false);
  const [student, setStudent] = useState(null);
  const [gpa, setGPA] = useState(null);

  const loadData = async () => {
    try {
      const studentData = await studentsService.getMe();
      setStudent(studentData);

      const gpaData = await studentsService.getGPA(studentData.id);
      setGPA(gpaData);
    } catch (error) {
      console.error('Error loading dashboard:', error);
    } finally {
      setLoading(false);
      setRefreshing(false);
    }
  };

  useEffect(() => {
    loadData();
  }, []);

  const onRefresh = () => {
    setRefreshing(true);
    loadData();
  };

  if (loading) {
    return (
      <View style={styles.loadingContainer}>
        <ActivityIndicator size="large" color="#2196F3" />
      </View>
    );
  }

  return (
    <ScrollView
      style={styles.container}
      refreshControl={
        <RefreshControl refreshing={refreshing} onRefresh={onRefresh} />
      }
    >
      <View style={styles.header}>
        <Text style={styles.welcome}>Welcome, {student?.name}!</Text>
        <Text style={styles.email}>{student?.email}</Text>
      </View>

      <View style={styles.gpaContainer}>
        <View style={styles.gpaCard}>
          <Text style={styles.gpaLabel}>GPA</Text>
          <Text style={styles.gpaValue}>{gpa?.gpa?.toFixed(2) || '0.00'}</Text>
        </View>
        <View style={styles.gpaCard}>
          <Text style={styles.gpaLabel}>CGPA</Text>
          <Text style={styles.gpaValue}>{gpa?.cgpa?.toFixed(2) || '0.00'}</Text>
        </View>
      </View>

      <View style={styles.statsContainer}>
        <StatCard
          title="Enrolled Courses"
          value={student?.enrolled_courses?.length || 0}
          color="#4CAF50"
        />
        <StatCard
          title="Total Grades"
          value={student?.grades?.length || 0}
          color="#FF9800"
        />
      </View>

      <View style={styles.section}>
        <Text style={styles.sectionTitle}>Recent Activity</Text>
        <Text style={styles.placeholder}>No recent activity</Text>
      </View>
    </ScrollView>
  );
}

function StatCard({ title, value, color }) {
  return (
    <View style={[styles.statCard, { borderLeftColor: color }]}>
      <Text style={styles.statValue}>{value}</Text>
      <Text style={styles.statTitle}>{title}</Text>
    </View>
  );
}

const styles = StyleSheet.create({
  container: {
    flex: 1,
    backgroundColor: '#f5f5f5',
  },
  loadingContainer: {
    flex: 1,
    justifyContent: 'center',
    alignItems: 'center',
  },
  header: {
    backgroundColor: '#2196F3',
    padding: 20,
    paddingTop: 40,
  },
  welcome: {
    fontSize: 24,
    fontWeight: 'bold',
    color: '#fff',
    marginBottom: 5,
  },
  email: {
    fontSize: 14,
    color: '#fff',
    opacity: 0.8,
  },
  gpaContainer: {
    flexDirection: 'row',
    padding: 20,
    gap: 15,
  },
  gpaCard: {
    flex: 1,
    backgroundColor: '#fff',
    padding: 20,
    borderRadius: 10,
    alignItems: 'center',
    shadowColor: '#000',
    shadowOffset: { width: 0, height: 2 },
    shadowOpacity: 0.1,
    shadowRadius: 4,
    elevation: 3,
  },
  gpaLabel: {
    fontSize: 14,
    color: '#666',
    marginBottom: 5,
  },
  gpaValue: {
    fontSize: 32,
    fontWeight: 'bold',
    color: '#2196F3',
  },
  statsContainer: {
    flexDirection: 'row',
    padding: 20,
    gap: 15,
  },
  statCard: {
    flex: 1,
    backgroundColor: '#fff',
    padding: 15,
    borderRadius: 10,
    borderLeftWidth: 4,
    shadowColor: '#000',
    shadowOffset: { width: 0, height: 2 },
    shadowOpacity: 0.1,
    shadowRadius: 4,
    elevation: 3,
  },
  statValue: {
    fontSize: 24,
    fontWeight: 'bold',
    color: '#333',
    marginBottom: 5,
  },
  statTitle: {
    fontSize: 12,
    color: '#666',
  },
  section: {
    padding: 20,
  },
  sectionTitle: {
    fontSize: 18,
    fontWeight: 'bold',
    marginBottom: 15,
    color: '#333',
  },
  placeholder: {
    textAlign: 'center',
    color: '#999',
    padding: 20,
  },
});
```

### Courses Screen

Create `app/(tabs)/courses.js`:
```javascript
import React, { useState, useEffect } from 'react';
import {
  View,
  Text,
  StyleSheet,
  FlatList,
  TouchableOpacity,
  RefreshControl,
  ActivityIndicator,
  Alert,
} from 'react-native';
import coursesService from '../../services/courses';
import studentsService from '../../services/students';

export default function CoursesScreen() {
  const [loading, setLoading] = useState(true);
  const [refreshing, setRefreshing] = useState(false);
  const [courses, setCourses] = useState([]);
  const [student, setStudent] = useState(null);

  const loadData = async () => {
    try {
      const studentData = await studentsService.getMe();
      setStudent(studentData);

      const coursesData = await coursesService.getCourses();
      setCourses(coursesData.results || coursesData);
    } catch (error) {
      console.error('Error loading courses:', error);
      Alert.alert('Error', 'Failed to load courses');
    } finally {
      setLoading(false);
      setRefreshing(false);
    }
  };

  useEffect(() => {
    loadData();
  }, []);

  const handleEnroll = async (courseId) => {
    try {
      await studentsService.enrollCourse(student.id, courseId);
      Alert.alert('Success', 'Enrolled in course successfully');
      loadData();
    } catch (error) {
      Alert.alert('Error', 'Failed to enroll in course');
    }
  };

  const renderCourse = ({ item }) => (
    <TouchableOpacity style={styles.courseCard}>
      <View style={styles.courseHeader}>
        <Text style={styles.courseName}>{item.name}</Text>
        <Text style={styles.courseCode}>{item.code}</Text>
      </View>
      <Text style={styles.lecturer}>Lecturer: {item.lecturer}</Text>
      <View style={styles.courseFooter}>
        <Text style={styles.credits}>{item.credit_units} Credits</Text>
        <Text style={styles.students}>{item.student_count} Students</Text>
      </View>
      <TouchableOpacity
        style={styles.enrollButton}
        onPress={() => handleEnroll(item.id)}
      >
        <Text style={styles.enrollButtonText}>Enroll</Text>
      </TouchableOpacity>
    </TouchableOpacity>
  );

  if (loading) {
    return (
      <View style={styles.loadingContainer}>
        <ActivityIndicator size="large" color="#2196F3" />
      </View>
    );
  }

  return (
    <View style={styles.container}>
      <FlatList
        data={courses}
        renderItem={renderCourse}
        keyExtractor={(item) => item.id.toString()}
        contentContainerStyle={styles.listContainer}
        refreshControl={
          <RefreshControl refreshing={refreshing} onRefresh={loadData} />
        }
        ListEmptyComponent={
          <Text style={styles.emptyText}>No courses available</Text>
        }
      />
    </View>
  );
}

const styles = StyleSheet.create({
  container: {
    flex: 1,
    backgroundColor: '#f5f5f5',
  },
  loadingContainer: {
    flex: 1,
    justifyContent: 'center',
    alignItems: 'center',
  },
  listContainer: {
    padding: 15,
  },
  courseCard: {
    backgroundColor: '#fff',
    borderRadius: 10,
    padding: 15,
    marginBottom: 15,
    shadowColor: '#000',
    shadowOffset: { width: 0, height: 2 },
    shadowOpacity: 0.1,
    shadowRadius: 4,
    elevation: 3,
  },
  courseHeader: {
    flexDirection: 'row',
    justifyContent: 'space-between',
    alignItems: 'center',
    marginBottom: 10,
  },
  courseName: {
    fontSize: 18,
    fontWeight: 'bold',
    color: '#333',
    flex: 1,
  },
  courseCode: {
    fontSize: 14,
    color: '#2196F3',
    fontWeight: '600',
  },
  lecturer: {
    fontSize: 14,
    color: '#666',
    marginBottom: 10,
  },
  courseFooter: {
    flexDirection: 'row',
    justifyContent: 'space-between',
    marginBottom: 10,
  },
  credits: {
    fontSize: 12,
    color: '#999',
  },
  students: {
    fontSize: 12,
    color: '#999',
  },
  enrollButton: {
    backgroundColor: '#4CAF50',
    padding: 10,
    borderRadius: 5,
    alignItems: 'center',
  },
  enrollButtonText: {
    color: '#fff',
    fontWeight: 'bold',
  },
  emptyText: {
    textAlign: 'center',
    color: '#999',
    marginTop: 50,
    fontSize: 16,
  },
});
```

---

## 🚀 Running the App

### Development

```bash
# Start Expo development server
npx expo start

# Or specific platforms
npx expo start --android
npx expo start --ios
npx expo start --web
```

### Testing

1. **On Physical Device:**
   - Install "Expo Go" app
   - Scan QR code from terminal
   - Ensure phone and computer on same WiFi

2. **On Simulator:**
   - Press `a` for Android emulator
   - Press `i` for iOS simulator

### Building for Production

```bash
# Build Android APK
eas build --platform android

# Build iOS IPA
eas build --platform ios

# Build both
eas build --platform all
```

---

## 📝 Next Steps

1. **Complete remaining screens:**
   - Grades screen
   - Profile screen
   - Course details screen
   - Review submission modal

2. **Add features:**
   - Push notifications
   - Offline support
   - Dark mode
   - Search and filters

3. **Testing:**
   - Unit tests with Jest
   - E2E tests with Detox
   - User testing

4. **Deployment:**
   - Submit to App Store
   - Submit to Google Play Store

---

**Your mobile app foundation is ready! Start building! 📱**
