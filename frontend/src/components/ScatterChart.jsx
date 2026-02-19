import { useState, useEffect } from 'react';
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
  us_low_cn_low: '两难探索型',
};

function useIsMobile() {
  const [isMobile, setIsMobile] = useState(window.innerWidth < 640);
  useEffect(() => {
    const onResize = () => setIsMobile(window.innerWidth < 640);
    window.addEventListener('resize', onResize);
    return () => window.removeEventListener('resize', onResize);
  }, []);
  return isMobile;
}

export default function ScatterChart({ chartData, quadrant, allPoints = [], exportMode = false }) {
  const { us_score, cn_score, threshold } = chartData;
  const userColor = QUADRANT_COLORS[quadrant] || '#3b82f6';
  const rawIsMobile = useIsMobile();
  // In export mode, always use desktop dimensions regardless of screen size
  const isMobile = exportMode ? false : rawIsMobile;

  // ---------- Trim outliers: drop top/bottom 3 by US score and CN score ----------
  const TRIM_N = 3;
  let filtered = allPoints;
  if (allPoints.length > TRIM_N * 4) {
    const byUs = [...allPoints].sort((a, b) => a.us_score - b.us_score);
    const byCn = [...allPoints].sort((a, b) => a.cn_score - b.cn_score);
    const outlierSet = new Set();
    // Bottom 3 and top 3 by US score
    for (let i = 0; i < TRIM_N; i++) {
      outlierSet.add(byUs[i]);
      outlierSet.add(byUs[byUs.length - 1 - i]);
    }
    // Bottom 3 and top 3 by CN score
    for (let i = 0; i < TRIM_N; i++) {
      outlierSet.add(byCn[i]);
      outlierSet.add(byCn[byCn.length - 1 - i]);
    }
    filtered = allPoints.filter((pt) => !outlierSet.has(pt));
  }

  // Group filtered points by quadrant
  const grouped = {};
  for (const q of Object.keys(QUADRANT_COLORS)) {
    grouped[q] = [];
  }
  for (const pt of filtered) {
    if (grouped[pt.quadrant]) {
      grouped[pt.quadrant].push([pt.cn_score, pt.us_score]);
    }
  }

  // Compute axis range from filtered data + user point
  const allUs = filtered.map((p) => p.us_score).concat([us_score]);
  const allCn = filtered.map((p) => p.cn_score).concat([cn_score]);
  const minVal = Math.floor(Math.max(0, Math.min(...allUs, ...allCn) - 10));
  const maxVal = Math.ceil(Math.max(...allUs, ...allCn) + 10);

  // Background scatter series for each quadrant
  const bgSeries = Object.entries(grouped).map(([q, points]) => ({
    type: 'scatter',
    name: QUADRANT_LABELS[q],
    symbolSize: isMobile ? 4 : 6,
    itemStyle: {
      color: QUADRANT_COLORS[q],
      opacity: 0.45,
    },
    data: points,
    z: 2,
  }));

  // Responsive sizes
  const gridConfig = isMobile
    ? { left: 45, right: 25, top: 55, bottom: 85 }
    : { left: 60, right: 60, top: 80, bottom: 145 };

  const titleFontSize = isMobile ? 14 : 18;
  const subtextFontSize = isMobile ? 10 : 12;
  const axisNameFontSize = isMobile ? 11 : 14;
  const axisLabelFontSize = isMobile ? 10 : 12;
  const legendFontSize = isMobile ? 10 : 11;
  const quadrantLabelFontSize = isMobile ? 10 : 13;
  const userLabelFontSize = isMobile ? 11 : 13;
  const userSymbolSize = isMobile ? 10 : 14;

  const option = {
    title: {
      text: '去留决策四象限图',
      subtext: `共 ${allPoints.length} 人参与测试`,
      left: 'center',
      top: isMobile ? 4 : 10,
      textStyle: { fontSize: titleFontSize, fontWeight: 'bold' },
      subtextStyle: { fontSize: subtextFontSize, color: '#999' },
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
      textStyle: { fontSize: legendFontSize },
      itemGap: isMobile ? 8 : 20,
      itemWidth: isMobile ? 12 : 25,
      itemHeight: isMobile ? 8 : 14,
    },
    grid: gridConfig,
    xAxis: {
      name: isMobile ? '中国 →' : '中国吸引力 →',
      nameLocation: 'middle',
      nameGap: isMobile ? 24 : 30,
      nameTextStyle: { fontSize: axisNameFontSize, fontWeight: 'bold' },
      min: minVal,
      max: maxVal,
      splitLine: { show: true, lineStyle: { color: '#f0f0f0' } },
      axisLine: { lineStyle: { color: '#999' } },
      axisLabel: { fontSize: axisLabelFontSize, formatter: (v) => Math.round(v) },
    },
    yAxis: {
      name: isMobile ? '美国 ↑' : '美国吸引力 ↑',
      nameLocation: 'end',
      nameGap: 15,
      nameTextStyle: {
        fontSize: axisNameFontSize,
        fontWeight: 'bold',
        align: 'left',
      },
      min: minVal,
      max: maxVal,
      splitLine: { show: true, lineStyle: { color: '#f0f0f0' } },
      axisLine: { lineStyle: { color: '#999' } },
      axisLabel: { fontSize: axisLabelFontSize, formatter: (v) => Math.round(v) },
    },
    // Quadrant background shading
    graphic: [
      // Left-top: 留美 (US high, CN low)
      {
        type: 'rect',
        left: gridConfig.left,
        top: gridConfig.top,
        shape: { width: '40%', height: '40%' },
        style: { fill: 'rgba(59,130,246,0.04)' },
        silent: true,
        z: -1,
      },
      // Right-top: 撕裂 (both high)
      {
        type: 'rect',
        right: gridConfig.right,
        top: gridConfig.top,
        shape: { width: '40%', height: '40%' },
        style: { fill: 'rgba(168,85,247,0.04)' },
        silent: true,
        z: -1,
      },
      // Left-bottom: 两难 (both low)
      {
        type: 'rect',
        left: gridConfig.left,
        bottom: gridConfig.bottom,
        shape: { width: '40%', height: '40%' },
        style: { fill: 'rgba(107,114,128,0.04)' },
        silent: true,
        z: -1,
      },
      // Right-bottom: 回国 (CN high, US low)
      {
        type: 'rect',
        right: gridConfig.right,
        bottom: gridConfig.bottom,
        shape: { width: '40%', height: '40%' },
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
          fontSize: quadrantLabelFontSize,
          color: '#bbb',
          fontWeight: 'bold',
        },
        tooltip: { show: false },
        data: [
          { name: '坚定留美派', value: [minVal + (isMobile ? 5 : 8), maxVal - 5] },
          { name: '果断回国派', value: [maxVal - (isMobile ? 5 : 8), minVal + 5] },
          { name: '跨国撕裂型', value: [maxVal - (isMobile ? 5 : 8), maxVal - 5] },
          { name: '两难探索型', value: [minVal + (isMobile ? 5 : 8), minVal + 5] },
        ],
      },
      // Background scatter dots per quadrant
      ...bgSeries,
      // User's highlighted point
      {
        type: 'effectScatter',
        name: '你的位置',
        symbolSize: userSymbolSize,
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
          fontSize: userLabelFontSize,
          fontWeight: 'bold',
          color: userColor,
          textBorderColor: '#fff',
          textBorderWidth: 3,
          textShadowColor: 'rgba(0,0,0,0.15)',
          textShadowBlur: 4,
        },
        z: 10,
        data: [[cn_score, us_score]],
      },
    ],
  };

  // Export mode uses taller height so the chart fills a 3:4 image nicely
  const chartHeight = exportMode ? 920 : (isMobile ? 420 : 780);

  return (
    <ReactECharts
      option={option}
      style={{ height: chartHeight, width: '100%' }}
      opts={{ renderer: 'canvas' }}
    />
  );
}
