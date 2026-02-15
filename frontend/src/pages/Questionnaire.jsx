import { useState, useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import { Button, Progress, Typography, message, Spin, Steps } from 'antd';
import { ArrowLeftOutlined, ArrowRightOutlined, SendOutlined } from '@ant-design/icons';
import QuestionCard from '../components/QuestionCard';
import { fetchQuestions, submitAnswers } from '../api';

const { Title, Text } = Typography;

const CATEGORY_ORDER = [
  '基础信息',
  '职业与财务硬件',
  '身份与生活方式',
  '家庭、情感与社会资本',
];

export default function Questionnaire() {
  const navigate = useNavigate();
  const [questions, setQuestions] = useState([]);
  const [answers, setAnswers] = useState({});
  const [loading, setLoading] = useState(true);
  const [submitting, setSubmitting] = useState(false);
  const [currentCategory, setCurrentCategory] = useState(0);

  useEffect(() => {
    fetchQuestions().then((data) => {
      setQuestions(data);
      // 初始化所有答案的默认权重
      const defaults = {};
      data.forEach((q) => {
        defaults[q.id] = { weight: 3 };
      });
      setAnswers(defaults);
      setLoading(false);
    });
  }, []);

  const handleAnswerChange = (questionId, value) => {
    setAnswers((prev) => ({ ...prev, [questionId]: value }));
  };

  // 按类别分组
  const groupedQuestions = CATEGORY_ORDER.map((cat) => ({
    category: cat,
    items: questions.filter((q) => q.category === cat),
  })).filter((g) => g.items.length > 0);

  const currentGroup = groupedQuestions[currentCategory];
  const totalQuestions = questions.length;
  const answeredCount = Object.values(answers).filter(
    (a) => a.selected_option || a.age
  ).length;
  const progress = totalQuestions > 0 ? Math.round((answeredCount / totalQuestions) * 100) : 0;

  const isCurrentGroupComplete = () => {
    if (!currentGroup) return false;
    return currentGroup.items.every((q) => {
      const a = answers[q.id];
      if (q.type === 'age_input') return a?.age !== undefined;
      return a?.selected_option !== undefined;
    });
  };

  const handleSubmit = async () => {
    // 验证所有题目都已作答
    const unanswered = questions.filter((q) => {
      const a = answers[q.id];
      if (q.type === 'age_input') return a?.age === undefined;
      return a?.selected_option === undefined;
    });

    if (unanswered.length > 0) {
      message.error(`还有 ${unanswered.length} 道题未作答，请完成所有题目。`);
      return;
    }

    setSubmitting(true);
    try {
      const ageAnswer = answers[0];
      const choiceAnswers = questions
        .filter((q) => q.type !== 'age_input')
        .map((q) => ({
          question_id: q.id,
          selected_option: answers[q.id].selected_option,
          weight: answers[q.id].weight || 3,
        }));

      const result = await submitAnswers({
        age: ageAnswer.age,
        age_weight: ageAnswer.weight || 3,
        answers: choiceAnswers,
      });

      navigate(`/result/${result.session_id}`, { state: result });
    } catch (err) {
      message.error('提交失败，请重试');
      console.error(err);
    } finally {
      setSubmitting(false);
    }
  };

  if (loading) {
    return (
      <div style={{ display: 'flex', justifyContent: 'center', alignItems: 'center', minHeight: '100vh' }}>
        <Spin size="large" />
      </div>
    );
  }

  return (
    <div style={{ maxWidth: 800, margin: '0 auto', padding: '24px 16px' }}>
      <Title level={3} style={{ textAlign: 'center', marginBottom: 8 }}>
        留学生去留决策量表
      </Title>

      <Progress
        percent={progress}
        format={() => `${answeredCount}/${totalQuestions}`}
        strokeColor={{ '0%': '#667eea', '100%': '#764ba2' }}
        style={{ marginBottom: 24 }}
      />

      <Steps
        current={currentCategory}
        size="small"
        style={{ marginBottom: 32 }}
        onChange={(idx) => setCurrentCategory(idx)}
        items={groupedQuestions.map((g) => ({ title: g.category }))}
      />

      {currentGroup && (
        <>
          <Title level={4} style={{ color: '#667eea', marginBottom: 24 }}>
            {currentGroup.category}
          </Title>

          {currentGroup.items.map((q, idx) => (
            <QuestionCard
              key={q.id}
              question={q}
              index={questions.findIndex((qq) => qq.id === q.id)}
              answer={answers[q.id]}
              onAnswerChange={handleAnswerChange}
            />
          ))}
        </>
      )}

      <div style={{ display: 'flex', justifyContent: 'space-between', marginTop: 32, marginBottom: 48 }}>
        <Button
          size="large"
          icon={<ArrowLeftOutlined />}
          disabled={currentCategory === 0}
          onClick={() => setCurrentCategory((c) => c - 1)}
        >
          上一部分
        </Button>

        {currentCategory < groupedQuestions.length - 1 ? (
          <Button
            type="primary"
            size="large"
            icon={<ArrowRightOutlined />}
            disabled={!isCurrentGroupComplete()}
            onClick={() => setCurrentCategory((c) => c + 1)}
          >
            下一部分
          </Button>
        ) : (
          <Button
            type="primary"
            size="large"
            icon={<SendOutlined />}
            loading={submitting}
            onClick={handleSubmit}
            style={{
              background: 'linear-gradient(135deg, #667eea 0%, #764ba2 100%)',
              border: 'none',
            }}
          >
            提交并查看结果
          </Button>
        )}
      </div>
    </div>
  );
}
