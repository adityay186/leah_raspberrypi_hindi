from crontab import CronTab

def create_cronjob(command, schedule, comment):
    cron = CronTab(user='leah')  # Specify the username whose cron jobs you want to modify

    # Check if cron job with the specified comment already exists
    for job in cron:
        if job.comment == comment:
            print(f"A cron job with comment '{comment}' already exists.")
            return "Daily Quote Service already exists"

    # Create a new cron job
    job = cron.new(command=command, comment=comment)

    # Set the schedule for the cron job
    job.setall(schedule)

    # Write the cron job to the cron tab
    cron.write()

    print("Cron job created successfully.")

    return "Daily Quote Service has been started"

def delete_cronjob(comment):
    cron = CronTab(user='leah')  # Specify the username whose cron jobs you want to modify

    # Check if cron job with the specified comment exists
    found = False
    for job in cron:
        if job.comment == comment:
            # Remove the cron job
            cron.remove(job)
            found = True

    if not found:
        print(f"No cron job with comment '{comment}' found.")
        return "No Daily Quote Service available to be deleted"

    # Write the updated cron jobs to the cron tab
    cron.write()

    print("Cron job deleted successfully.")

    return "Daily Quote service has been stopped"

def flip(intent_dict):
    command = '/home/leah/miniforge3/bin/python /home/leah/Documents/leah-final-hindi/skills/quotes.py'
    schedule = '24 12 * * *'
    comment = 'daily_quotes'

    action = intent_dict['dailyQuotesAction']
    tts = intent_dict['tts_obj']

    if action == 'start':
        # Check if cron job already exists before creating it
        cron = CronTab(user='leah')
        for job in cron:
            if job.comment == comment:
                tts.text = "the quote service is already enabled"
                tts.play()
                print(f"A cron job with comment '{comment}' already exists.")
                return

        # Create the cron job
        create_cronjob(command, schedule, comment)
        tts.text = "the quote service is now enabled"
        tts.play()

    elif action == 'stop':
        # Check if cron job exists before deleting it
        cron = CronTab(user='leah')
        found = False
        for job in cron:
            if job.comment == comment:
                # Delete the cron job
                cron.remove(job)
                found = True

        if not found:
            tts.text = "the quote service is already disabled"
            tts.play()
            print(f"No cron job with comment '{comment}' found.")
            return

        # Write the updated cron jobs to the cron tab
        cron.write()

        tts.text = "the quote service is now disabled"
        tts.play()
        print("Cron job deleted successfully.")

    else:
        tts.text = "that's an invalid action"
        print("Invalid action.")

