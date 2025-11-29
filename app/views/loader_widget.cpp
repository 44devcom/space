#include "loader_widget.h"
#include <QPainter>
#include <QPen>
#include <QBrush>
#include <cmath>

#ifndef M_PI
#define M_PI 3.14159265358979323846
#endif

LoaderWidget::LoaderWidget(QWidget *parent)
    : QWidget(parent)
    , m_rotation_angle(0)
    , m_is_animating(false)
{
    setFixedSize(60, 60);
    
    m_animation = new QPropertyAnimation(this, "rotation_angle", this);
    m_animation->setDuration(1000);
    m_animation->setStartValue(0);
    m_animation->setEndValue(360);
    m_animation->setLoopCount(-1); // Infinite loop
}

LoaderWidget::~LoaderWidget()
{
    stop_animation();
}

void LoaderWidget::set_rotation_angle(int angle)
{
    m_rotation_angle = angle;
    update();
}

void LoaderWidget::start_animation()
{
    if (!m_is_animating) {
        m_animation->start();
        m_is_animating = true;
    }
}

void LoaderWidget::stop_animation()
{
    if (m_is_animating) {
        m_animation->stop();
        m_is_animating = false;
    }
}

void LoaderWidget::paintEvent(QPaintEvent *event)
{
    Q_UNUSED(event)
    
    QPainter painter(this);
    painter.setRenderHint(QPainter::Antialiasing);
    
    int center_x = width() / 2;
    int center_y = height() / 2;
    int radius = qMin(width(), height()) / 2 - 5;
    
    painter.translate(center_x, center_y);
    painter.rotate(m_rotation_angle);
    painter.translate(-center_x, -center_y);
    
    QPen pen;
    pen.setWidth(4);
    pen.setCapStyle(Qt::RoundCap);
    
    // Draw animated circle segments
    for (int i = 0; i < 8; ++i) {
        float alpha = 1.0f - (i / 8.0f);
        pen.setColor(QColor(100, 150, 255, static_cast<int>(255 * alpha)));
        painter.setPen(pen);
        
        float angle = (i * 45.0f) * M_PI / 180.0f;
        float start_angle = angle;
        float span_angle = 30.0f * M_PI / 180.0f;
        
        QRectF rect(center_x - radius, center_y - radius, radius * 2, radius * 2);
        painter.drawArc(rect, static_cast<int>(start_angle * 16 * 180 / M_PI), 
                       static_cast<int>(span_angle * 16 * 180 / M_PI));
    }
}

