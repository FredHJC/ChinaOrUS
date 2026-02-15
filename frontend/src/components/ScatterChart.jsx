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

export default function ScatterChart({ chartData, quadrant }) {
  const { us_score, cn_score, threshold } = chartData;
  const color = QUADRANT_COLORS[quadrant] || '#3b82f6';

  const option = {
    title: {
      text: '去留决策四象限图',
      left: 'center',
      top: 10,
      textStyle: { fontSize: 18, fontWeight: 'bold' },
    },
    grid: {
      left: 80,
      right: 60,
      top: 60,
      bottom: 80,
    },
    xAxis: {
      name: '中国吸引力 →',
      nameLocation: 'middle',
      nameGap: 40,
      min: 5,
      max: 225,
      splitLine: { show: false },
      axisLine: { lineStyle: { color: '#999' } },
    },
    yAxis: {
      name: '↑ 美国吸引力',
      nameLocation: 'middle',
      nameGap: 50,
      min: 5,
      max: 225,
      splitLine: { show: false },
      axisLine: { lineStyle: { color: '#999' } },
    },
    // 四象限背景区域
    graphic: [
      // 左上 - 留美
      {
        type: 'rect',
        left: 80,
        top: 60,
        shape: { width: '42%', height: '42%' },
        style: { fill: 'rgba(59,130,246,0.06)' },
        silent: true,
        z: -1,
      },
      // 右上 - 撕裂
      {
        type: 'rect',
        right: 60,
        top: 60,
        shape: { width: '42%', height: '42%' },
        style: { fill: 'rgba(168,85,247,0.06)' },
        silent: true,
        z: -1,
      },
      // 左下 - 双输
      {
        type: 'rect',
        left: 80,
        bottom: 80,
        shape: { width: '42%', height: '42%' },
        style: { fill: 'rgba(107,114,128,0.06)' },
        silent: true,
        z: -1,
      },
      // 右下 - 回国
      {
        type: 'rect',
        right: 60,
        bottom: 80,
        shape: { width: '42%', height: '42%' },
        style: { fill: 'rgba(239,68,68,0.06)' },
        silent: true,
        z: -1,
      },
    ],
    series: [
      // 中轴线 (十字线)
      {
        type: 'line',
        markLine: {
          silent: true,
          symbol: 'none',
          lineStyle: { color: '#ddd', type: 'dashed', width: 1 },
          data: [
            { xAxis: threshold },
            { yAxis: threshold },
          ],
          label: { show: false },
        },
        data: [],
      },
      // 象限文字标注
      {
        type: 'scatter',
        symbolSize: 0,
        label: {
          show: true,
          formatter: '{b}',
          fontSize: 12,
          color: '#bbb',
        },
        data: [
          { name: '坚定留美派', value: [25, 200] },
          { name: '果断回国派', value: [200, 25] },
          { name: '跨国撕裂型', value: [200, 200] },
          { name: '破局重组派', value: [25, 25] },
        ],
      },
      // 用户数据点
      {
        type: 'effectScatter',
        symbolSize: 20,
        rippleEffect: { brushType: 'stroke', scale: 3 },
        itemStyle: { color },
        label: {
          show: true,
          position: 'right',
          formatter: '你的位置',
          fontSize: 14,
          fontWeight: 'bold',
          color,
        },
        data: [[cn_score, us_score]],
      },
    ],
  };

  return (
    <ReactECharts
      option={option}
      style={{ height: 500, width: '100%' }}
      opts={{ renderer: 'canvas' }}
    />
  );
}
