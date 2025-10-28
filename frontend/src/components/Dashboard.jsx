import React from 'react';

function Dashboard({ data, platform }) {
  if (!data) return null;

  const { daily_statistics, peak_activity, weekday_patterns, data_quality, time_span } = data;

  return (
    <div className="space-y-6">
      {/* Header */}
      <div className="bg-white rounded-lg shadow-md p-6">
        <h2 className="text-2xl font-bold text-gray-900">
          Activity Analysis Dashboard
        </h2>
        <p className="text-gray-600 mt-2">
          Data from {platform.name}
        </p>
      </div>

      {/* Daily Statistics */}
      <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
        <div className="bg-white rounded-lg shadow-md p-6">
          <h3 className="text-lg font-semibold text-gray-700 mb-2">
            Mean Daily Steps
          </h3>
          <p className="text-3xl font-bold text-blue-600">
            {daily_statistics.mean_steps.toFixed(0)}
          </p>
        </div>

        <div className="bg-white rounded-lg shadow-md p-6">
          <h3 className="text-lg font-semibold text-gray-700 mb-2">
            Median Daily Steps
          </h3>
          <p className="text-3xl font-bold text-green-600">
            {daily_statistics.median_steps.toFixed(0)}
          </p>
        </div>

        <div className="bg-white rounded-lg shadow-md p-6">
          <h3 className="text-lg font-semibold text-gray-700 mb-2">
            Peak Activity (Interval)
          </h3>
          <p className="text-3xl font-bold text-purple-600">
            {peak_activity.interval}
          </p>
          <p className="text-sm text-gray-500 mt-1">
            {peak_activity.average_steps.toFixed(1)} avg steps
          </p>
        </div>
      </div>

      {/* Weekday vs Weekend */}
      <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
        <div className="bg-white rounded-lg shadow-md p-6">
          <h3 className="text-lg font-semibold text-gray-700 mb-4">
            Weekday Patterns
          </h3>
          <div className="text-2xl font-bold text-indigo-600">
            {weekday_patterns.weekday_avg.toFixed(1)}
          </div>
          <p className="text-sm text-gray-500">Average steps per interval</p>
        </div>

        <div className="bg-white rounded-lg shadow-md p-6">
          <h3 className="text-lg font-semibold text-gray-700 mb-4">
            Weekend Patterns
          </h3>
          <div className="text-2xl font-bold text-pink-600">
            {weekday_patterns.weekend_avg.toFixed(1)}
          </div>
          <p className="text-sm text-gray-500">Average steps per interval</p>
        </div>
      </div>

      {/* Data Quality */}
      <div className="bg-white rounded-lg shadow-md p-6">
        <h3 className="text-lg font-semibold text-gray-700 mb-4">
          Data Quality Metrics
        </h3>
        <div className="space-y-2">
          <div className="flex justify-between">
            <span className="text-gray-600">Data Completeness</span>
            <span className="font-bold text-green-600">
              {data_quality.data_completeness.toFixed(1)}%
            </span>
          </div>
          <div className="flex justify-between">
            <span className="text-gray-600">Total Data Points</span>
            <span className="font-bold text-blue-600">
              {data_quality.total_rows.toLocaleString()}
            </span>
          </div>
          <div className="flex justify-between">
            <span className="text-gray-600">Missing Data Points</span>
            <span className="font-bold text-orange-600">
              {data_quality.missing_steps}
            </span>
          </div>
        </div>
      </div>

      {/* Time Span */}
      <div className="bg-white rounded-lg shadow-md p-6">
        <h3 className="text-lg font-semibold text-gray-700 mb-4">
          Analysis Period
        </h3>
        <div className="space-y-2">
          <div className="flex justify-between">
            <span className="text-gray-600">Start Date</span>
            <span className="font-semibold">{time_span.start_date}</span>
          </div>
          <div className="flex justify-between">
            <span className="text-gray-600">End Date</span>
            <span className="font-semibold">{time_span.end_date}</span>
          </div>
          <div className="flex justify-between">
            <span className="text-gray-600">Total Days</span>
            <span className="font-semibold">{time_span.total_days}</span>
          </div>
        </div>
      </div>
    </div>
  );
}

export default Dashboard;

