import tensorflow as tf

graph = tf.Graph()
with graph.as_default():
    with tf.name_scope('Variables'):
        global_step = tf.Variable(0,dtype=tf.int32,trainable=False,name='global_step')
        total_output = tf.Variable(0.0,dtype=tf.float32,trainable=False,name='total_output')

    with tf.name_scope('Transformation') as transformation:
        #Separate input layer
        with tf.name_scope('input'):
            a = tf.placeholder(dtype = tf.float32, shape=[None], name = 'input_placeholder_a')

        #Separate middle layer
        with tf.name_scope('intermediate_layer'):
            b = tf.reduce_prod(a,name = 'product_b')
            c = tf.reduce_sum(a, name = 'sum_c')

        #Separate output layer
        with tf.name_scope('output'):
            output = tf.add(b,c,name='output')

    with tf.name_scope('update'):
        #Increments the total_output Variable by the lastest output
        update_total = total_output.assign_add(output)
        #Increments the above 'global_step' Variable,should be run whenever the graph is run
        increment_step = global_step.assign_add(1)
    with tf.name_scope('summaries'):
        avg = tf.div(update_total,tf.cast(increment_step,tf.float32),name='average')
        output_summary = tf.summary.scalar(name='Output',tensor=output)
        total_summary = tf.summary.scalar(name='Sum of outputs over time',tensor=update_total)
        average_summary = tf.summary.scalar(name='Average of outputs over time',tensor=avg)

    with tf.name_scope('global_ops'):
        #Initialization Op
        init = tf.global_variables_initializer()
        merged_summaries = tf.summary.merge_all

sess = tf.Session(graph=graph)

writer = tf.summary.FileWriter('./improved_graph',graph= graph)

sess.run(init)

def run_graph(input_tensor):
    feed_dict = {a:input_tensor}
    # tf.run(output,feed_dict=feed_dict)
    # _,step,summary = sess.run([output,increment_step,merged_summaries],feed_dict=feed_dict)
    # writer.add_summary(summary,global_step = step)
    pass

run_graph([2,8])