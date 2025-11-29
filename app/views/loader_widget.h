#ifndef LOADER_WIDGET_H
#define LOADER_WIDGET_H

#include <QWidget>
#include <QPropertyAnimation>
#include <QTimer>

class LoaderWidget : public QWidget
{
    Q_OBJECT
    Q_PROPERTY(int rotation_angle READ rotation_angle WRITE set_rotation_angle)

public:
    explicit LoaderWidget(QWidget *parent = nullptr);
    ~LoaderWidget();

    int rotation_angle() const { return m_rotation_angle; }
    void set_rotation_angle(int angle);

    void start_animation();
    void stop_animation();

protected:
    void paintEvent(QPaintEvent *event) override;

private:
    int m_rotation_angle;
    QPropertyAnimation *m_animation;
    bool m_is_animating;
};

#endif // LOADER_WIDGET_H

