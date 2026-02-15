import ReactECharts from 'echarts-for-react';

const QUADRANT_COLORS = {
  us_high_cn_low: '#3b82f6',
  us_low_cn_high: '#ef4444',
  us_high_cn_high: '#a855f7',
  us_low_cn_low: '#6b7280',
};

const QUADRANT_LABELS = {
  us_high_cn_low: '坚定留美派',
  us_low_cn_high: '果断回国派',
  us_high_cn_high: '跨国撕裂型',
  us_low_cn_low: '破局重组派',
};

export default function ScatterChart({ chartData, quadrant, allPoints = [] }) {
  const { us_score, cn_score, threshold } = chartData;
  const userColor = QUADRANT_COLORS[quadrant] || '#3b82f6';

  // Group all historical points by quadrant
  const grouped = {};
  for (const q of Object.keys(QUADRANT_COLORS)) {
    grouped[q] = [];
  }
  for (const pt of allPoints) {
    if (grouped[pt.quadrant]) {
      grouped[pt.quadrant].push([pt.cn_score, pt.us_score]);
    }
  }

  // Compute axis range from all data (round to integers)
  const allUs = allPoints.map((p) => p.us_score).concat([us_score]);
  const allCn = allPoints.map((p) => p.cn_score).concat([cn_score]);
  const minVal = Math.floor(Math.max(0, Math.min(...allUs, ...allCn) - 10));
  const maxVal = Math.ceil(Math.max(...allUs, ...allCn) + 10);

  // Background scatter series for each quadrant
  const bgSeries = Object.entries(grouped).map(([q, points]) => ({
    type: 'scatter',
    name: QUADRANT_LABELS[q],
    symbolSize: 6,
    itemStyle: {
      color: QUADRANT_COLORS[q],
      opacity: 0.45,
    },
    data: points,
    z: 2,
  }));

  const option = {
    title: {
      text: '去留决策四象限图',
      subtext: `共 ${allPoints.length} 人参与测试`,
      left: 'center',
      top: 10,
      textStyle: { fontSize: 18, fontWeight: 'bold' },
      subtextStyle: { fontSize: 12, color: '#999' },
    },
    tooltip: {
      trigger: 'item',
      formatter: (params) => {
        if (params.seriesName === '你的位置') {
          return `<b>你的位置</b><br/>中国吸引力: ${params.value[0]}<br/>美国吸引力: ${params.value[1]}`;
        }
        return `${params.seriesName}<br/>中国: ${params.value[0]}, 美国: ${params.value[1]}`;
      },
    },
    legend: {
      bottom: 0,
      data: Object.values(QUADRANT_LABELS),
      textStyle: { fontSize: 11 },
      itemGap: 20,
    },
    grid: {
      left: 80,
      right: 60,
      top: 80,
      bottom: 100,
    },
    xAxis: {
      name: '中国吸引力 →',
      nameLocation: 'middle',
      nameGap: 45,
      nameTextStyle: { fontSize: 14, fontWeight: 'bold' },
      min: minVal,
      max: maxVal,
      splitLine: { show: true, lineStyle: { color: '#f0f0f0' } },
      axisLine: { lineStyle: { color: '#999' } },
      axisLabel: { formatter: (v) => Math.round(v) },
    },
    yAxis: {
      name: '↑ 美国吸引力',
      nameLocation: 'middle',
      nameGap: 50,
      nameTextStyle: { fontSize: 14, fontWeight: 'bold' },
      min: minVal,
      max: maxVal,
      splitLine: { show: true, lineStyle: { color: '#f0f0f0' } },
      axisLine: { lineStyle: { color: '#999' } },
      axisLabel: { formatter: (v) => Math.round(v) },
    },
    // Quadrant background shading
    graphic: [
      // Left-top: 留美 (US high, CN low)
      {
        type: 'rect',
        left: 80,
        top: 80,
        shape: { width: '42%', height: '42%' },
        style: { fill: 'rgba(59,130,246,0.04)' },
        silent: true,
        z: -1,
      },
      // Right-top: 撕裂 (both high)
      {
        type: 'rect',
        right: 60,
        top: 80,
        shape: { width: '42%', height: '42%' },
        style: { fill: 'rgba(168,85,247,0.04)' },
        silent: true,
        z: -1,
      },
      // Left-bottom: 双输 (both low)
      {
        type: 'rect',
        left: 80,
        bottom: 60,
        shape: { width: '42%', height: '42%' },
        style: { fill: 'rgba(107,114,128,0.04)' },
        silent: true,
        z: -1,
      },
      // Right-bottom: 回国 (CN high, US low)
      {
        type: 'rect',
        right: 60,
        bottom: 60,
        shape: { width: '42%', height: '42%' },
        style: { fill: 'rgba(239,68,68,0.04)' },
        silent: true,
        z: -1,
      },
    ],
    series: [
      // Threshold cross lines
      {
        type: 'line',
        markLine: {
          silent: true,
          symbol: 'none',
          lineStyle: { color: '#333', type: 'dashed', width: 1.5, opacity: 0.6 },
          data: [
            { xAxis: threshold },
            { yAxis: threshold },
          ],
          label: { show: false },
        },
        data: [],
      },
      // Quadrant text labels
      {
        type: 'scatter',
        symbolSize: 0,
        label: {
          show: true,
          formatter: '{b}',
          fontSize: 13,
          color: '#bbb',
          fontWeight: 'bold',
        },
        tooltip: { show: false },
        data: [
          { name: '坚定留美派', value: [minVal + 8, maxVal - 5] },
          { name: '果断回国派', value: [maxVal - 8, minVal + 5] },
          { name: '跨国撕裂型', value: [maxVal - 8, maxVal - 5] },
          { name: '破局重组派', value: [minVal + 8, minVal + 5] },
        ],
      },
      // Background scatter dots per quadrant
      ...bgSeries,
      // User's highlighted point
      {
        type: 'effectScatter',
        name: '你的位置',
        symbolSize: 14,
        rippleEffect: { brushType: 'stroke', scale: 2.5, period: 4 },
        itemStyle: {
          color: userColor,
          shadowBlur: 8,
          shadowColor: userColor,
          borderColor: '#fff',
          borderWidth: 2,
        },
        label: {
          show: true,
          position: 'right',
          formatter: '你的位置',
          fontSize: 13,
          fontWeight: 'bold',
          color: userColor,
        },
        z: 10,
        data: [[cn_score, us_score]],
      },
    ],
  };

  return (
    <ReactECharts
      option={option}
      style={{ height: 560, width: '100%' }}
      opts={{ renderer: 'canvas' }}
    />
  );
}
