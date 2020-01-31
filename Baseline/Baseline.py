
import StimToolLib, os, random, operator
from psychopy import visual, core, event, data, gui

#slide show module: just presents a slide show (of flowers) for baseline phsyio recording

class GlobalVars:
    #This class will contain all module specific global variables
    #This way, all of the variables that need to be accessed in several functions don't need to be passed in as parameters
    #It also avoids needing to declare every global variable global at the beginning of every function that wants to use it
    def __init__(self):
        self.cues = None #shape cues
        self.text_cues = None #numerical cues under the shapes-
        self.win = None #the window where everything is drawn

event_types = {'INSTRUCT_ONSET':1, 
    'TASK_ONSET':2, 
    'IMAGE_ONSET':3,
    'TASK_END':StimToolLib.TASK_END}
    
def run(session_params, run_params):
    global g
    g = GlobalVars()
    g.session_params = session_params
    g.run_params = StimToolLib.get_var_dict_from_file(os.path.dirname(__file__) + '/PB.Default.params', {})
    g.run_params.update(run_params)
    try:
        run_try()
        g.status = 0
    except StimToolLib.QuitException as q:
        g.status = -1
    StimToolLib.task_end(g)
    return g.status
        
def run_try():  
#def run_try(SID, raID, scan, resk):

    schedules = [f for f in os.listdir(os.path.dirname(__file__)) if f.endswith('.schedule')]
    if not g.session_params['auto_advance']:
        myDlg = gui.Dlg(title="PB")
        myDlg.addField('Run Number', choices=schedules, initial=g.run_params['run'])
        myDlg.show()  # show dialog and wait for OK or Cancel
        if myDlg.OK:  # then the user pressed OK
            thisInfo = myDlg.data
        else:
            print 'QUIT!'
            return -1#the user hit cancel so exit 
        g.run_params['run'] = thisInfo[0]
    
    
    StimToolLib.general_setup(g)
    schedule_file = os.path.join(os.path.dirname(__file__), g.run_params['run'])
    #schedule_file = os.path.join(os.path.dirname(__file__),'T1000_Physio_Baseline_Schedule1.csv')
    trial_types,images,durations,junk = StimToolLib.read_trial_structure(schedule_file, g.win, g.msg)

    g.mask = visual.ImageStim(g.win, image=os.path.join(os.path.dirname(__file__), 'media', 'mask.bmp'), mask=os.path.join(os.path.dirname(__file__), 'media', 'mask_mask.bmp')) #used to crop the images to 1024x768

    
    durations = durations[0] #in this case, we only have a single image and a single duration per trial
    images = images[0]
    
    start_time = data.getDateStr()
    
    param_file = g.run_params['run'][0:-9] + '.params' #every .schedule file can (probably should) have a .params file associated with it to specify running parameters (including part of the output filename)
    StimToolLib.get_var_dict_from_file(os.path.join(os.path.dirname(__file__), param_file), g.run_params)
    g.prefix = StimToolLib.generate_prefix(g)
    fileName = os.path.join(g.prefix + '.csv')
    
    #g.prefix = 'PB-' + g.session_params['SID'] + '-Admin_' + str(g.session_params['raID']) + '-run_1' + '-' +  start_time 
    #fileName = os.path.join(os.path.dirname(__file__), 'data/' + g.prefix +  '.csv')
    g.output= open(fileName, 'w')
    sorted_events = sorted(event_types.iteritems(), key=operator.itemgetter(1))
    g.output.write('Administrator:,' + g.session_params['admin_id'] + ',Original File Name:,' + fileName + ',Time:,' + start_time + ',Parameter File:,' +  schedule_file + ",Event Codes:," + str(sorted_events) + '\n')
    g.output.write('trial_number,trial_type,event_code,absolute_time,response_time,response,result\n')
    StimToolLib.task_start(StimToolLib.BASELINE_CODE, g) #send message that this task is starting
    
    instruct_onset = g.clock.getTime()
    StimToolLib.mark_event(g.output, 'NA', 'NA', event_types['INSTRUCT_ONSET'], instruct_onset, 'NA', 'NA', 'NA', g.session_params['signal_parallel'], g.session_params['parallel_port_address'])
    StimToolLib.run_instructions(os.path.join(os.path.dirname(__file__), 'media', 'instructions', 'PB_instruct_schedule.csv'), g)
    #StimToolLib.show_title(g.win, g.title)
    #StimToolLib.show_instructions(g.win, g.instructions)
    if g.session_params['scan']:
        StimToolLib.wait_scan_start(g.win)
    else:
        StimToolLib.wait_start(g.win)
    instruct_end = g.clock.getTime()
    StimToolLib.mark_event(g.output, 'NA', 'NA', event_types['TASK_ONSET'], instruct_end, instruct_end - instruct_onset, 'NA', 'NA', g.session_params['signal_parallel'], g.session_params['parallel_port_address'])
    g.trial = 0
    g.ideal_trial_start = instruct_end
    for i,d in zip(images, durations):
        
        i.draw()
        g.mask.draw()
        g.win.flip()
        StimToolLib.mark_event(g.output, g.trial, 0, event_types['IMAGE_ONSET'], g.clock.getTime(), 'NA', 'NA', i._imName, g.session_params['signal_parallel'], g.session_params['parallel_port_address'])
        #try:
        StimToolLib.just_wait(g.clock, g.ideal_trial_start + d)
        #except StimToolLib.QuitException as e:
        #    g.win.close()
        #    return -1
        g.ideal_trial_start = g.ideal_trial_start + d
        g.trial = g.trial + 1

  
 


