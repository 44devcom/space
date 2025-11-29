#ifndef BACKGROUND_3D_WIDGET_H
#define BACKGROUND_3D_WIDGET_H

#include <QOpenGLWidget>
#include <QOpenGLFunctions>
#include <QTimer>
#include <QMatrix4x4>

class Background3DWidget : public QOpenGLWidget, protected QOpenGLFunctions
{
    Q_OBJECT

public:
    explicit Background3DWidget(QWidget *parent = nullptr);
    ~Background3DWidget();

protected:
    void initializeGL() override;
    void resizeGL(int w, int h) override;
    void paintGL() override;

private:
    QTimer *m_timer;
    float m_rotation_angle;
    QMatrix4x4 m_projection;
    QMatrix4x4 m_view;
    QMatrix4x4 m_model;

    void setup_projection(int width, int height);
    void draw_cube();
};

#endif // BACKGROUND_3D_WIDGET_H

