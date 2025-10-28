import React from 'react';
import { LineChart, Line, BarChart, Bar, XAxis, YAxis, CartesianGrid, Tooltip, Legend, ResponsiveContainer } from 'recharts';

function ActivityCharts({ data }) {
  if (!data || !data.weekday_patterns) return null;

  const { weekday_intervals, weekend_intervals } = data.weekday_patterns;

  // Prepare interval data for charting
  const weekdayData = weekday_intervals.map(item => ({
    interval: item.interval,
    steps: parseFloat(item.steps)
  }));

  const weekendData = weekend_intervals.map(item => ({
    interval: item.interval,
    steps: parseFloat(item.steps)
  }));

  return (
    <div className="space-y-6 mt-8">
      <h2 className="text-2xl font-bold text-gray-900 mb-4">
        Activity Patterns
      </h2>

      {/* Weekday vs Weekend Comparison */}
      <div className="bg-white rounded-lg shadow-md p-6">
        <h3 className="text-lg font-semibold text-gray-700 mb-4">
          Weekday vs Weekend Activity Patterns
        </h3>
        <ResponsiveContainer width="100%" height={400}>
          <LineChart data={[...weekdayData, ...weekendData]}>
            <CartesianGrid strokeDasharray="3 3" />
            <XAxis 
              dataKey="interval" 
              label={{ value: 'Time Interval', position: 'insideBottom', offset: -5 }}
            />
            <YAxis label={{ value: 'Steps', angle: -90, position: 'insideLeft' }} />
            <Tooltip />
            <Legend />
            <Line type="monotone" dataKey="steps" stroke="#8884d8" name="Average Steps" />
          </LineChart>
        </ResponsiveContainer>
      </div>

      {/* Peak Activity Hours */}
      <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
        <div className="bg-white rounded-lg shadow-md p-6">
          <h3 className="text-lg font-semibold text-gray-700 mb-4">
            Weekday Activity Distribution
          </h3>
          <ResponsiveContainer width="100%" height={300}>
            <BarChart data={weekdayData.slice(0, 48)}>
              <CartesianGrid strokeDasharray="3 3" />
              <XAxis dataKey="interval" />
              <YAxis />
              <Tooltip />
              <Bar dataKey="steps" fill="#8884d8" />
            </BarChart>
          </ResponsiveContainer>
        </div>

        <div className="bg-white rounded-lg shadow-md p-6">
          <h3 className="text-lg font-semibold text-gray-700 mb-4">
            Weekend Activity Distribution
          </h3>
          <ResponsiveContainer width="100%" height={300}>
            <BarChart data={weekendData.slice(0, 48)}>
              <CartesianGrid strokeDasharray="3 3" />
              <XAxis dataKey="interval" />
              <YAxis />
              <Tooltip />
              <Bar dataKey="steps" fill="#82ca9d" />
            </BarChart>
          </ResponsiveContainer>
        </div>
      </div>
    </div>
  );
}

export default ActivityCharts;

